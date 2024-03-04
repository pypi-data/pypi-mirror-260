import os

import psutil

from basics.logging_utils import log_exception
from basics.logging import get_logger

import torch

import mlpug.pytorch as mlp

from mlpug.debugging import enable_pycharm_remote_debugging

from examples.persona_chatbot.training_process import TrainingProcess as TrainingProcessBase
from examples.persona_chatbot.pytorch.collation import BatchCollator

from examples.persona_chatbot.pytorch.shared_args import create_arg_parser, describe_args

module_logger = get_logger(os.path.basename(__file__))


try:
    import torch

    import torch.distributed as dist
    import torch.multiprocessing as mp

    from torch.nn.parallel import DistributedDataParallel as DDP

    from torch.optim import AdamW

    from torch.optim.lr_scheduler import LambdaLR

    from torch.nn.functional import softmax
except Exception as e:
    log_exception(module_logger, "Please install PyTorch, see https://pytorch.org/get-started/locally/", e)


try:
    from transformers import GPT2Config, GPT2Tokenizer, GPT2DoubleHeadsModel
    from transformers.trainer_pt_utils import get_parameter_names
except Exception as e:
    log_exception(module_logger, "Please `pip install transformers`", e)


def worker_fn(rank, args, world_size):
    if args.remote_debug_ip and rank == 0:
        enable_pycharm_remote_debugging(args.remote_debug_ip)

    mlp.logging.use_fancy_colors()

    training_process = TrainingProcess(rank, args, num_devices=world_size)
    training_process.setup()
    training_process.start()


def gather_next_sentence_prediction_data(batch, auxiliary_results, **kwargs):
    # Batch is a tuple with the following items :
    # [0] input_ids_batch,
    # [1] token_type_ids_batch,
    # [2] token_labels_ids_batch,
    # [3] last_token_idx_batch,
    # [4] reply_class_batch

    targets = batch[4]

    nsp_logits = auxiliary_results["nsp_logits"]

    prediction_probability = softmax(nsp_logits, dim=1)
    predictions = torch.argmax(prediction_probability, dim=1)

    return targets, predictions


def clean_up_batch_data(model_output, **kwargs):
    loss = model_output["loss"]

    model_output["loss"] = loss.cpu().item()

    # We don't need the auxiliary_results anymore
    del model_output["auxiliary_results"]


# MLPug needs a TrainModel that outputs the loss
class TrainModel(torch.nn.Module):
    def __init__(self, model, lm_loss_weight, device, activation_checkpointing=False):
        super(TrainModel, self).__init__()

        self.model = model
        self.lm_loss_weight = lm_loss_weight
        self.device = device

        self.activation_checkpointing = activation_checkpointing

    def forward(self, batch_data, evaluate_settings, inference_mode=None):
        batch_data = (tensor.to(self.device) for tensor in batch_data)

        input_ids_batch, \
            token_type_ids_batch, \
            token_labels_ids_batch, \
            last_token_idx_batch, \
            reply_class_batch = batch_data

        results = self.model(
            input_ids=input_ids_batch,
            token_type_ids=token_type_ids_batch,
            labels=token_labels_ids_batch,
            mc_token_ids=last_token_idx_batch,
            mc_labels=reply_class_batch,
            use_cache=not self.activation_checkpointing)

        loss = (results.loss*self.lm_loss_weight+results.mc_loss)/(self.lm_loss_weight+1.0)

        return {
            "loss": loss,
            "num_samples": input_ids_batch.shape[0],
            "auxiliary_results": {
                # required to calculate next sentence prediction (classification) quality
                # Detach graph to reduce memory usage
                "nsp_logits": results.mc_logits.detach()
            }
        }


# See TrainingProcessBase for more information on the different methods implemented here.
# Here we implement the methods that are specific to our problem and specific to our ML library, PyTorch.
class TrainingProcess(TrainingProcessBase):

    MLPUG_MODULE = mlp

    def __init__(self, rank, args, num_devices, name="PTTrainingProcess"):
        super().__init__(rank, args, num_devices, name=name)

        self._training_sampler = None
        self._validation_sampler = None

    def _setup_compute(self):
        cuda_available = torch.cuda.is_available()
        mps_available = torch.backends.mps.is_available()

        # Optimizations
        if cuda_available and not self._args.force_on_cpu:
            torch.set_float32_matmul_precision('high')

        if self._args.distributed:
            self._log.info(f"Distributed Data Parallel (DDP) mode.")

            os.environ['MASTER_ADDR'] = 'localhost'
            os.environ['MASTER_PORT'] = '12355'

            if cuda_available and not self._args.force_on_cpu:
                torch.cuda.set_device(self.rank)
                self._device = torch.device("cuda")

                backend = 'nccl'

                self._log.info(f"Training using multiple GPUs: Using GPU {self.rank}/{self.num_devices}")
            else:
                self._device = torch.device(f"cpu")
                backend = 'gloo'
                num_cores = psutil.cpu_count(logical=True)
                # Data loader workers per training worker
                num_dataloader_workers = max(self._args.num_dataloader_workers, 0)
                num_threads = max(int(num_cores/self.num_devices)-num_dataloader_workers, 1)
                torch.set_num_threads(num_threads)

                self._log.info(f"Training using multiple CPU cores: Worker {self.rank}/{self.num_devices}")
                self._log.info(f"Number of threads per worker: {num_threads}")

            dist.init_process_group(backend=backend,
                                    rank=self.rank,
                                    world_size=self.num_devices)

            self._log.info(f"Communication backend used for DDP: {backend}")
        else:
            if cuda_available and not self._args.force_on_cpu:
                self._device = torch.device("cuda")
                self._log.info(f"Single device mode : Using GPU")
            elif mps_available and not self._args.force_on_cpu:
                self._device = torch.device("mps")
                self._log.info(f"Single device mode : Using available Apple MPS device")
            else:
                self._device = torch.device("cpu")
                self._log.info(f"Single device mode : Using CPU")

    def _execute_for_primary_device_first(self, func, *args, **kwargs):
        # In distributed training mode, we allow the primary process to download or generate and cache any data first.
        # After that the secondary processes can load the data.
        if self.is_distributed and not self.is_primary:
            dist.barrier()

        results = func(*args, **kwargs)

        if self.is_distributed and self.is_primary:
            dist.barrier()

        return results

    def _setup_tokenizer(self):
        return self._execute_for_primary_device_first(super()._setup_tokenizer)

    def _generate_dataset(self, manager, dataset_name):
        return self._execute_for_primary_device_first(super()._generate_dataset, manager, dataset_name)

    def _setup_batch_datasets(self):
        if self.is_distributed:
            self._training_sampler = torch.utils.data.distributed.DistributedSampler(self._training_set)
            self._validation_sampler = torch.utils.data.distributed.DistributedSampler(self._validation_set)

        self._batch_training_set = torch.utils.data.DataLoader(
            self._training_set,
            batch_size=self._args.batch_size,
            shuffle=False,  # Samples already shuffled
            sampler=self._training_sampler,
            num_workers=self._args.num_dataloader_workers,
            collate_fn=BatchCollator(
                pad_token_idx=self._hf_tokenizer.pad_token_id,
                max_sequence_length=self._opt_max_sequence_length),
            pin_memory=True)

        # Using the test set as a validation set, just for demonstration purposes
        self._batch_validation_set = torch.utils.data.DataLoader(
            self._validation_set,
            batch_size=self._args.batch_size,
            shuffle=False,  # Samples already shuffled
            sampler=self._validation_sampler,
            num_workers=self._args.num_dataloader_workers,
            collate_fn=BatchCollator(
                pad_token_idx=self._hf_tokenizer.pad_token_id,
                max_sequence_length=self._opt_max_sequence_length),
            pin_memory=True)

    def _build_model(self):
        if self.is_distributed and not self.is_primary:
            dist.barrier()

        model_config = self._gather_model_config()

        self._log.info(f"Loading pre-trained GPT-2 model : {self._args.pretrained_model}")
        # Load pre-trained GPT-2 model
        self._model = GPT2DoubleHeadsModel.from_pretrained(self._args.pretrained_model, config=model_config)

        self._model.resize_token_embeddings(new_num_tokens=self._orig_num_tokens + self._num_special_tokens)

        self._log.info(f"Configuration of loaded model : \n{model_config}")

        if self._args.activation_checkpointing:
            self._model.gradient_checkpointing_enable()

        if self.is_distributed and self.is_primary:
            dist.barrier()

    def _setup_training_model(self):
        self._training_model = TrainModel(
            self._model,
            self._args.lm_loss_weight,
            self._device,
            activation_checkpointing=self._args.activation_checkpointing)

        self._training_model.to(self._device)
        if self.is_distributed:
            device_ids = [self.rank] if self._device.type == 'cuda' else None
            self._training_model = DDP(self._training_model, device_ids=device_ids)

    def _build_optimizer(self):
        # Adapted from Huggingface Transformers package v4.17, Trainer::create_optimizer, transformers/trainer.py:827
        decay_parameters = get_parameter_names(self._model, [torch.nn.LayerNorm])
        decay_parameters = [name for name in decay_parameters if "bias" not in name]
        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self._model.named_parameters() if n in decay_parameters],
                "weight_decay": self._args.weight_decay,
            },
            {
                "params": [p for n, p in self._model.named_parameters() if n not in decay_parameters],
                "weight_decay": 0.0,
            },
        ]

        self._optimizer = AdamW(optimizer_grouped_parameters, **{
            "lr": self._args.learning_rate,
            "betas": (0.9, 0.999),
            "eps": 1e-8,
        })

    def _create_gather_classification_data_function(self):
        return gather_next_sentence_prediction_data

    def _create_gather_distributed_classification_data_function(self):
        # Use default implementation made available by MLPug
        return mlp.evaluation.GatherDistributedTensorTuple(self._device)

    def _create_clean_up_batch_data_func(self):
        return clean_up_batch_data

    def _get_compile_kwargs(self):
        return {}

    def _get_custom_evaluator_config(self):
        return {
            "compile_kwargs": self._get_compile_kwargs()
        }

    def _get_custom_trainer_config(self):
        """
        Implementation depends on specific ML Library you are using

        :return:
        """
        return {
            "compile_kwargs": self._get_compile_kwargs()
        }

    def _setup_callbacks(self):
        super()._setup_callbacks()

        if self.is_distributed:
            # These callbacks provide the current epoch to the DistributedSampler to re-randomize the samples
            # in every epoch. They are added before the other callbacks
            self._callbacks = [
                mlp.callbacks.DistributedSamplerManager(
                    self._training_sampler,
                    name="DistributedSamplerManager[training]"),
                mlp.callbacks.DistributedSamplerManager(
                    self._validation_sampler,
                    name="DistributedSamplerManager[validation]")
            ] + self._callbacks

    def _add_lr_scheduler_callback(self):
        """
        Returns function that can cleanup the batch data to optimize memory use

        Implementation depends on specific ML Library you are using

        :return:
        """
        # See https://github.com/pytorch/pytorch/issues/120934#issuecomment-1973390203
        lr_scheduling_func = lambda iter: torch.tensor(self._lr_scheduling_func(iter), requires_grad=False)
        self._callbacks += [mlp.callbacks.LRSchedulerWrapper({
                'warmup-scheduler': LambdaLR(self._optimizer, lr_scheduling_func)
            }, batch_level=True)]

    @staticmethod
    def get_logger_info(rank, num_devices, name):
        """

        :param rank:
        :param num_devices:
        :param name:

        :return: (Logger name: String, disable_logging: Boolean)
        """

        if num_devices > 1:
            return f"[Device {rank}/{num_devices}] {name}", rank != 0
        else:
            return name, False


if __name__ == '__main__':
    # ############# SETUP LOGGING #############
    mlp.logging.use_fancy_colors()
    logger = get_logger(os.path.basename(__file__))
    # ########################################

    # ############## PARSE ARGS ##############
    parser = create_arg_parser()

    parser.parse_args()

    args = parser.parse_args()

    describe_args(args, logger)

    if args.remote_debug_ip:
        enable_pycharm_remote_debugging(args.remote_debug_ip)

    if not args.eager_mode and args.activation_checkpointing:
        raise ValueError("Currently activation checkpointing doesn't work with graph compilation.")

    # ############## TRAIN MODEL ##############
    cuda_available = torch.cuda.is_available()
    mps_available = torch.backends.mps.is_available()
    if args.distributed:

        if cuda_available and not args.force_on_cpu:
            # System with Nvidia GPUs
            num_devices_available = torch.cuda.device_count()
        else:
            # Need to manually provide number of devices
            num_devices_available = None

        if num_devices_available is not None and num_devices_available < 1:
            logger.error(f"--distributed flag set, but {num_devices_available} device available, unable to train")
            exit(-1)

        world_size = (
            args.num_devices if args.num_devices is not None and args.num_devices > 0
            else num_devices_available
        )

        if world_size is None:
            logger.error(f"The number of devices available could not be determined, please set --num-devices manually.")

        # Only on systems with GPUs we can't scale beyond number of GPUs. On CPU, we could divide the available cores
        # over different training processes.
        if cuda_available and not args.force_on_cpu and world_size > num_devices_available:
            logger.warning(f"Number of requested devices is higher than available devices, "
                           f"limiting training to {num_devices_available} devices")
            world_size = num_devices_available

        logger.info(f"Spawning {world_size} training workers.")
        logger.info(f"Global batch size: {args.batch_size*world_size}")

        mp.spawn(worker_fn,
                 args=(args, world_size,),
                 nprocs=world_size,
                 join=True)
    else:
        logger.info(f"Single device mode.")
        logger.info(f"Global batch size: {args.batch_size}")

        worker_fn(0, args=args, world_size=1)
