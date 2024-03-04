import sys
import abc

from typing import Optional, Iterable, Tuple, Dict, Collection, Union

import numpy as np

from mlpug.base import Base
import basics.base_utils as _

from mlpug.batch_chunking import (
    ChunkableBatch,
    BatchChunkingResults,
    ChunkableBatchDataset,
    ChunkableBatchWrapper,
    is_chunkable,
    convert_to_chunkable_dataset,
    ChunkableBatchDatasetInterface
)

from mlpug.mlpug_exceptions import InvalidParametersException
from mlpug.utils import *


class GatherLoss(Base):
    def __init__(self, requester=None, name="GatherLoss", **kwargs):
        if requester is not None:
            name += f'[{requester}]'

        super().__init__(pybase_logger_name=name, **kwargs)

        self.requester = requester

    def __call__(self, loss, num_samples, **kwargs):
        """
        Gathers the loss sum over the samples and the number of samples

        :param loss:
        :param num_samples:
        :param kwargs:
        :return:
        """
        # Convert back from average to loss sum
        return num_samples*loss, num_samples


# DEFAULT LOSS METRIC FUNCTION
def average_loss(metrics_inputs: Optional[Tuple]):
    if metrics_inputs is None:
        return metrics_inputs

    loss_sum, tot_num_samples = metrics_inputs
    return loss_sum/tot_num_samples


def do_nothing(**kwargs):
    pass


def overlapping_metrics(metric_names1, metric_names2):
    """
    Returns all metric names that are in metric_names1 and in metric_names2, in order of metric_names1
    :param metric_names1:
    :param metric_names2:
    :return:
    """

    return [name for name in metric_names1 if name in metric_names2]


class CombineBatchData(metaclass=abc.ABCMeta):

    def __init__(self, dim: int = 0):
        """
        :param dim: dimension of to concatenate the numpy arrays over, if relevant
        """
        self.dim = dim

    @abc.abstractmethod
    def __call__(self, iterable: Optional[Iterable[Collection]]) -> Optional[Collection]:
        """
        Assumes that the input is a iterable of batch data, where each batch data object contains items that are
        numpy arrays and/or int/float scalars.

        If the input iterable is None it returned immediately

        When a batch data item value is a numpy array, the array values for this item are concatenated
        When a batch data item value is a float/int scalar, the array values for this item are summed

        In other cases no specific combination is made, these item values will just be combined in to a list.

        :param iterable:
        :return:
        """
        raise NotImplementedError("Please implement in your child class.")

    def _concat(self, list_of_items):
        try:
            first_item = next(iter(list_of_items))
        except StopIteration:
            return list_of_items

        if isinstance(first_item, (float, int, np.number)):
            return sum(list_of_items)
        elif isinstance(first_item, np.ndarray):
            return np.concatenate(list_of_items, axis=self.dim)
        else:
            return self._handle_other_type(list_of_items, first_item=first_item)

    def _handle_other_type(self, list_of_items, first_item=None):
        return list_of_items


class CombineBatchTuples(CombineBatchData):

    def __call__(self, tuples: Optional[Iterable[Tuple]]) -> Optional[Tuple]:
        """

        Assumes that batch data in the iterable are tuples.
        Also see CombineBatchData.

        :param tuples:    Real world example, with first item NOT a numpy array or int/float scalar:
                          [
                              # Batch 1
                              (labels Numpy Array, predictions Numpy array, num_samples int, other data type),
                              ...
                              # Batch M
                              (labels Numpy Array, predictions Numpy array, num_samples int, other data type),
                          ]

        :return: Result for real world example:
                 (all M label numpy arrays concatenated,
                  all M prediction numpy arrays concatenated,
                  all M num_samples summed,
                  all M values of other data type in a list)

                 Returns None when the input tuples is None

        """
        if tuples is None:
            return tuples

        lists_of_items = zip(*tuples)

        return tuple(self._concat(list_of_items) for list_of_items in lists_of_items)


class CombineBatchDicts(CombineBatchData):

    def __call__(self, dicts: Optional[Iterable[Dict]]) -> Optional[Dict]:
        """

        Assumes that batch data in the iterable are dict's.
        Also see CombineBatchData.

        :param dicts:     Real world example:
                          [
                              {
                                "labels": Batch 1 Numpy Array with labels,
                                "predictions": Batch 1 Numpy Array with predictions,
                                "num_samples": Batch 1 num. samples (int),
                                "other_data": Batch 1 other data not of type Numpy Array or scalar
                              },
                              ...
                              {
                                "labels": Batch M Numpy Array with labels,
                                "predictions": Batch M Numpy Array with predictions,
                                "num_samples": Batch M num. samples (int),
                                "other_data": Batch 1 other data not of type Numpy Array or scalar
                              }
                          ]

        :return: Result for real world example:
                {
                    "labels": all M label numpy arrays concatenated,
                    "predictions": all M prediction numpy arrays concatenated,
                    "num_samples": sum of all M num_samples,
                    "other_data": all M values of other data type in a list
                }

                Returns None when the input dicts is None
        """
        if dicts is None:
            return dicts

        try:
            first_dict = next(iter(dicts))
            keys = first_dict.keys()
        except StopIteration:
            return {}

        lists_of_items = zip(*[d.values() for d in dicts])

        return {key: self._concat(list_of_items) for key, list_of_items in zip(keys, lists_of_items)}


class MetricEvaluator(Base, metaclass=abc.ABCMeta):

    def __init__(self,
                 model_evaluate_func=None,
                 trainer=None,
                 gather_metric_inputs_funcs=None,
                 gather_distributed_inputs_funcs=None,
                 clean_up_batch_data_func=None,
                 combine_metric_inputs_funcs=None,
                 combine_metric_inputs_func=None,
                 metric_funcs=None,
                 eager_mode: bool = False,
                 batch_chunk_size=None,
                 chunkable_batch_wrapper: Optional[ChunkableBatchWrapper] = None,
                 show_progress=False,
                 name="MetricEvaluator",
                 **kwargs):

        """

        A MetricEvaluator can evaluate metrics using the batch data and the training model output.
        It can do this at different levels:
         * Metrics calculation on the level of a single batch, either directly or
           by first chunking the batch in to smaller batch chunks (to reduce memory usage)

         * Metrics calculation on the level of multiple batches, e.g. over a dataset or window of batches

        To evaluate the metrics, the MetricEvaluator, needs a way to evaluate the training model.
        This is done by either providing a model_evaluate_func, or a trainer instance, since a trainer
        knows how to evaluate the training model.


        In order to accurately calculate the metrics of interest, combining all the samples in a batch, or batches,
        we call a few different types of functions in order:

         1) `gather_metric_inputs_funcs`, a dict with, for each metric, a function that can
            gather inputs, from the batch data and model output, to calculate the metric of interest with

         2) `gather_distributed_inputs_funcs`, a dict with, for each metric, a function that can
            gather the metric inputs from different devices in a distributed computing context, if applicable

         3) `clean_up_batch_data_func`, an optional function that can be used to clean-up batch data
             that is not used any more after gathering the metric inputs. This is useful to optimize memory usage.

         4) `combine_metric_inputs_funcs`, a dict with, for each metric, a function that can
            combine metric inputs from multiple batches, e.g. data from multiple batch chunks, batches of a dataset,
            or of a window of batches.

         5) `metric_funcs`, a dict with, for each metric, a function to
            calculate the metric based on the gathered/combined metric inputs

        In a default situation, for loss no functions need to be provided, defaults are available for all functions
        For other metrics, at least a gather_metric_inputs_func and a metric_func needs to be provided.

        In summary, for each metric the functions are called as follows:
        batch_metric_inputs = gather_metric_inputs_func(batch, evaluate_settings, loss, num_samples, auxiliary_results)
        batch_metric_inputs = gather_distributed_inputs_func(batch_metric_inputs)

        In case of calculating metrics for a single batch:
            metric = metric_func(batch_metric_inputs)

        In case of calculating metrics over multiple batches, or batch chunks:
            combined_metric_inputs = combine_metric_inputs_func([batch_metric_inputs1, ..., batch_metric_inputsM])
            metric = metric_func(combined_metric_inputs)

        Hence, the data structure of batch_metric_inputs and combined_metric_inputs must be the same.


        :param model_evaluate_func: Optional. f(batch_data, evaluate_settings) -> model_output
            Instead of providing a model_evaluate_func, you can provide a trainer instance.
            Also see below.

            IMPORTANT: it is assumed that the `model_evaluate_func` takes all
            appropriate measures to disable training specific layers such as
            dropout and gradient calculations.

            Eg. for Pytorch:

            def eval_model(batch_data, evaluate_settings):

                my_training_model.eval()

                with torch.no_grad():
                    return my_training_model(batch_data, evaluate_settings)

        :param trainer: An optional trainer instance to evaluate a model.
            You can provide this instead of a custom model_evaluate_func
            If no batch_chunk_size and chunkable_batch_wrapper are given in the constructor (see description below)
            we will get this values from the trainer, if set.

        :param gather_metric_inputs_funcs: A dict with keys representing the metric names
            (e.g. "loss", "classification", etc.), the values are functions that can
            gather inputs, from the batch data and model output, to calculate the metric of interest with

            In general there is no strict signature for the functions here.
            However, for defaults the following is assumed:
                func(batch, evaluate_settings, loss, num_samples, auxiliary_results) -> Tuple[Union[T, int, float]]
                Where T is a Tensor.

            Default: If no gather_metric_inputs_funcs are provided, a default implementation to only gather
            loss data is used.

            The functions will be called as follows:

                gather_metric_inputs_func(**kwargs)

                Where kwargs will contain the following keys:
                'batch', 'evaluate_settings' and the keys of the model evaluation results, see model_evaluate_func
                This is the 'loss', 'num_samples' and 'auxiliary_results'.

                Example gather_batch_data_funcs dict:

                    def gather_loss_data(batch, loss, **kwargs):
                        inputs = batch[0]
                        num_samples = inputs.shape[1]

                        return loss, num_samples

                    def gather_classification_data(batch, auxiliary_results, **kwargs):
                        target = batch[1]
                        predicted = auxiliary_results[0]

                        return target, predicted

                    gather_batch_data_funcs = {
                        'loss': gather_loss_data,
                        'classification': gather_classification_data
                    }

        :param gather_distributed_inputs_funcs: A dict with keys representing the metric names
            (e.g. "loss", "classification", etc.), the values are functions that can
            gather the metric inputs from different devices in a distributed computing context, if applicable.

            In general there is no strict signature for the functions here.
            However for defaults, the following is assumed:
                gather_func(gathered_input_data: Tuple[Union[T, float, int]]) -> Tuple[Union[T, float, int]]
                Where T is a Tensor type.

            Per Deep Learning library a default implementation is provided for this parameter.

        :param clean_up_batch_data_func: An optional function that can be used to clean-up batch data
            that is not used any more after gathering the metric inputs. This is useful to optimize memory usage.

            The following function signature is assumed:
                func(batch, evaluate_settings, model_output) -> None

                Where model_output is a dict:
                {'loss': <loss tensor>, 'num_samples': <int>, 'auxiliary_results': <Any>}

                The model_output is the original dict as stored in the logs object, so
                removing or replacing data in this dict will effect the data in the logs object.

        :param combine_metric_inputs_funcs: A dict with keys representing the metric names
            (e.g. "loss", "classification", etc.), the values are functions that can
            combine metric inputs from multiple batches, e.g. data from multiple batch chunks, batches of a dataset,
            or of a window of batches.

            In general there is no strict signature for the functions here.
            However, for defaults, the following is assumed:
                combine_func(gathered_input_data: Iterable[Tuple[Union[T, float, int]]])
                    -> Tuple[Union[Iterable, T, float, int]]
                Where T is a Tensor type (numpy arrays are also allowed)

            Default: If no combine_metric_inputs_funcs are provided, the defaults are as follows:
                * for 'loss': the loss and num_samples are summed over all batch data given using `CombineBatchTuples`
                * for other metrics: it is assumed that the output of the gather_batch_data_funcs are
                  tuples of Tensors of the Deep Learning library used (numpy arrays are also allowed).

                To do this `CombineBatchTuples` is also used here.

            Per Deep Learning library a default implementation is provided for this parameter.

        :param combine_metric_inputs_func: Instead of `combine_metric_inputs_funcs`, you can provide
            one function that will be used by all metrics defined in `gather_metric_inputs_funcs`

        :param metric_funcs: A dict with keys representing the metric names
            (e.g. "loss", "classification", etc.), the values are functions to
            calculate the metric based on the gathered/combined metric inputs

            In general there is no strict signature for the functions here.
            However, for defaults, the following is assumed:
                metric_func(combined_input_data: Tuple[Union[Iterable, T, float, int]]) -> Union[M, Tuple[M], Dict[M]]
                Where M is a scalar float/int/numpy.number

            Default: If no metric_funcs are provided, the defaults are as follows:
                * for 'loss': the average loss is calculated; it is assumed that
                * for other metrics: it is assumed that the output of the gather_batch_data_funcs are
                  tuples of Tensors of the Deep Learning library used (numpy arrays are also allowed).

                  To do this `CombineBatchTuples` is also used here.

            Example metric_funcs dict:

                def average_loss(combined_metric_inputs):
                    loss_sum, tot_num_samples = combined_metric_inputs

                    return loss_sum/tot_num_samples

                def calc_classification_quality(combined_metric_inputs):
                    target, predicted = combined_metric_inputs

                    recall, precision = ... calculate precision and recall based in target and predicted ...

                    return {
                        'recall': recall,
                        'precision': precision
                    }

                metric_funcs = {
                    'loss': average_loss,
                    'classification': calc_classification_quality
                }

            NOTE :
             * When a tuple is returned, the LogProgress logger will always only print the first value in the tuple
             * When a dict is returned, the LogProgress logger will print values for all keys in the dict
               (e.g. recall and precision)

        :param eager_mode: If true, the evaluation is not compiled

        :param batch_chunk_size: If given, batches will be evaluated by chunking it to
                 smaller batches of size batch_chunk_size

                 When specifying this option, you can specify batch_chunk_metric_reducer_funcs.
                 The way the batch is evaluated works as follows:

                 for all chunks in batch:
                    eval chunk
                    use eval result to calculate batch metrics with batch_metric_funcs

                 Reduce all batch metric results of the chunks using batch_chunk_metric_reducer_funcs

                 If not given, but a trainer is given, the batch_chunk_size of the trainer is used

        :type batch_chunk_size: int

        :param chunkable_batch_wrapper: Optional wrapper, making batches chunkable.
            This is required when a batch_chunk_size is given and batches are not already chunkable when
            provided for evaluation

            If not given, but a trainer is given, the chunkable_batch_wrapper of the trainer is used

        :param show_progress If True, the progress of dataset evaluation will be logged
        :type show_progress
        """

        super().__init__(pybase_logger_name=name, **kwargs)

        self._trainer = None
        if trainer is not None:
            if model_evaluate_func is not None:
                raise InvalidParametersException("Either provide a trainer instance or a model_evaluate_func, not both")

            self._trainer = trainer

            self._model_evaluate_func = self._create_default_model_evaluate_func()
        else:
            if not callable(model_evaluate_func):
                raise InvalidParametersException("If no trainer object is provided, "
                                                 "you should provide a callable model_evaluate_func")

            self._model_evaluate_func = model_evaluate_func

        try:
            if gather_metric_inputs_funcs is None:
                gather_metric_inputs_funcs = {
                    "loss": GatherLoss(requester=name)
                }

            self.check_funcs(gather_metric_inputs_funcs)
        except InvalidParametersException as e:
            raise InvalidParametersException("The gather metric inputs funcs are invalid") from e

        metric_names = gather_metric_inputs_funcs.keys()

        if type(gather_distributed_inputs_funcs) is not dict:
            raise InvalidParametersException("No gather_distributed_inputs_funcs dict provided")

        # For the different deep learning library backends supported, defaults should be provided
        for metric_name in metric_names:
            if metric_name not in gather_distributed_inputs_funcs:
                raise InvalidParametersException(
                    f'No gather_distributed_inputs_func provided for metric : {metric_name}')

        try:
            self.check_funcs(gather_distributed_inputs_funcs, func_names=gather_metric_inputs_funcs.keys())
        except InvalidParametersException as e:
            raise InvalidParametersException("There are issues with the provided gather_distributed_inputs_funcs") \
                from e

        if not callable(clean_up_batch_data_func):
            clean_up_batch_data_func = do_nothing

        # For the different deep learning library backends supported, defaults should be provided
        if combine_metric_inputs_funcs is None:
            if callable(combine_metric_inputs_func):
                combine_metric_inputs_funcs = {metric_name: combine_metric_inputs_func for metric_name in metric_names}
            else:
                raise InvalidParametersException("Either provide one combine_metric_inputs_func or "
                                                 "the combine_metric_inputs_funcs dict")
        elif callable(combine_metric_inputs_func):
            raise InvalidParametersException("Either provide one combine_metric_inputs_func or "
                                             "the combine_metric_inputs_funcs dict, not both.")

        for metric_name in metric_names:
            if metric_name not in combine_metric_inputs_funcs:
                raise InvalidParametersException(f'No combine_metric_inputs_func provided for metric : {metric_name}')

        try:
            self.check_funcs(combine_metric_inputs_funcs, func_names=gather_metric_inputs_funcs.keys())
        except InvalidParametersException as e:
            raise InvalidParametersException("There are issues with the provided combine_metric_inputs_funcs") \
                from e

        for metric_name in metric_names:
            if metric_name not in metric_funcs:
                raise InvalidParametersException(f'No metric_func provided for metric : {metric_name}')

        try:
            self.check_funcs(metric_funcs, func_names=gather_metric_inputs_funcs.keys())
        except InvalidParametersException as e:
            raise InvalidParametersException("There are issues with the provided metric_funcs") \
                from e

        self._gather_metric_inputs_funcs = gather_metric_inputs_funcs
        self._gather_distributed_inputs_funcs = gather_distributed_inputs_funcs
        self._clean_up_batch_data_func = clean_up_batch_data_func
        self._combine_metric_inputs_funcs = combine_metric_inputs_funcs
        self._metric_funcs = metric_funcs

        self._eager_mode = eager_mode

        if batch_chunk_size is None and self._trainer is not None:
            batch_chunk_size = self._trainer.batch_chunk_size

            if batch_chunk_size is not None:
                self._log.info(f"Using batch_chunk_size of the given trainer: {batch_chunk_size}")

        if chunkable_batch_wrapper is None and self._trainer is not None:
            chunkable_batch_wrapper = self._trainer.chunkable_batch_wrapper

            if chunkable_batch_wrapper is not None:
                self._log.info(f"Using chunkable_batch_wrapper of the given trainer: {chunkable_batch_wrapper}")

        self._batch_chunk_size = batch_chunk_size
        self._chunkable_batch_wrapper = chunkable_batch_wrapper

        self._show_progress = show_progress

        self._name = name

    def get_name(self):
        return self._name

    def get_metric_names(self):
        """
        Get the names of the metrics that are calculated by this `MetricEvaluator`.

        :return:
        :rtype:
        """
        return list(self._gather_metric_inputs_funcs.keys())

    def gather_batch_metric_inputs(self,
                                   batch_data=None,
                                   model_output: Optional[Dict] = None,
                                   evaluate_settings=None,
                                   skip_metrics=None,
                                   no_chunking=False):
        """

        :param batch_data:
        :param model_output: Optional, externally calculated model output
                              This is used as an alternative to giving the batch_data
        :type model_output: Optional[Dict]

        :param evaluate_settings:
        :param skip_metrics: Optional List of metric names to skip calculating the metrics for
        :param no_chunking:

        :return: (gathered inputs, success boolean)
                  gathered inputs is a Dict or None
        """

        if not no_chunking and model_output is None and self._batch_chunk_size is not None:
            chunk_dataset = self._create_chunkable_batch_dataset(batch_data)

            gathered_inputs, success = self.gather_dataset_metric_inputs(
                dataset=chunk_dataset,
                evaluate_settings=evaluate_settings,
                skip_metrics=skip_metrics,
                show_progress=False,
                no_chunking=True,
                dataset_name="batch chunks")

            if not success:
                self._log.error(f"Gathering of metric inputs from batch chunks failed")
                return gathered_inputs, False

            gathered_inputs, success = self.combine_gathered_metric_inputs(
                gathered_inputs,
                "batch chunks",
                show_progress=False)

            if not success:
                self._log.error(f"Combining metric inputs of batch chunks failed")

            return gathered_inputs, success

        if is_chunkable(batch_data):
            # The batch is chunkable but, we are not using the chunks: get the full batch.
            batch_data = batch_data[:]

        if skip_metrics is None:
            skip_metrics = []

        if model_output is None:
            try:
                model_output = self._model_evaluate_func(batch_data, evaluate_settings)
            except Exception as e:
                _.log_exception(self._log, "Evaluating model on batch input data failed", e)
                return None, False

        if not isinstance(model_output, dict):
            self._log.error(
                f"Given model_output is not a dict, "
                f"unable to gather batch metric inputs: \n{model_output}"
            )
            return None, False

        metric_func_args = {**model_output, **{
            'batch': batch_data,
            'evaluate_settings': evaluate_settings
        }}

        gathered_inputs = {}
        success = True
        for metric_name, gather_metric_inputs_func in self._gather_metric_inputs_funcs.items():
            if metric_name in skip_metrics:
                continue

            try:
                metric_inputs = gather_metric_inputs_func(**metric_func_args)

                gather_distributed_inputs_func = self._gather_distributed_inputs_funcs[metric_name]
                metric_inputs = gather_distributed_inputs_func(metric_inputs)

                gathered_inputs[metric_name] = metric_inputs
            except Exception as e:
                _.log_exception(self._log, f"Gathering inputs for metric {metric_name} failed", e)
                success = False

        try:
            self._clean_up_batch_data_func(
                batch=batch_data,
                evaluate_settings=evaluate_settings,
                model_output=model_output)

        except Exception as e:
            _.log_exception(self._log, f"Cleaning up batch data failed (ignoring this failure)", e)

        return gathered_inputs, success

    def gather_dataset_metric_inputs(self,
                                     dataset: Optional[Iterable] = None,
                                     model_outputs: Optional[Iterable[Dict]] = None,
                                     evaluate_settings=None,
                                     skip_metrics=None,
                                     no_chunking=False,
                                     dataset_name=None,
                                     show_progress=None):
        """
        Gathers the batch metric inputs over the dataset provided

        :param dataset: Iterable batch dataset

        :param model_outputs: Optional, externally calculated model outputs
                              This is used as an alternative to giving the dataset
        :type model_outputs: Optional[Iterable[Dict]]

        :param evaluate_settings:
        :param skip_metrics: Optional List of metric names to skip calculating the metrics for
        :param no_chunking:
        :param dataset_name:
        :param show_progress:

        :return: Tuple:
                    Dict with, per metric, list of gathered inputs over dataset
                    Boolean indicating success

        """

        success = False
        gathered_metric_inputs = {}

        if dataset is not None and model_outputs is not None:
            self._log.error("Either provide a dataset or a list of model outputs, not both")
            return gathered_metric_inputs, success

        if dataset is not None and not hasattr(dataset, '__iter__'):
            self._log.error(f"The given dataset {str(dataset)} is not iterable, "
                            f"unable to gather metric inputs over dataset")
            return gathered_metric_inputs, success

        if model_outputs is not None and not hasattr(model_outputs, '__iter__'):
            self._log.error(f"The given model_outputs for dataset {str(dataset)} is not iterable, "
                            f"unable to gather metric inputs over dataset")
            return gathered_metric_inputs, success

        dataset_desc = 'dataset' if dataset_name is None else f'{dataset_name} dataset'

        if show_progress is None:
            show_progress = self._show_progress

        if show_progress:
            metric_names = self.get_metric_names()
            self._log.debug(f"Gathering batch metric inputs ({', '.join(metric_names)}) over the {dataset_desc}")

            self._write_to_stdout('\n')

        def gather_metrics_for(batch=None, model_output=None):
            all_batch_metric_inputs, success = self.gather_batch_metric_inputs(
                batch_data=batch,
                model_output=model_output,
                evaluate_settings=evaluate_settings,
                skip_metrics=skip_metrics,
                no_chunking=no_chunking)

            if not success:
                self._log.error(f"Gathering of batch metric inputs failed, will stop gathering "
                                f"metric inputs over the {dataset_desc}")
                return False

            for metric_name, batch_metric_inputs in all_batch_metric_inputs.items():
                if metric_name not in gathered_metric_inputs:
                    gathered_metric_inputs[metric_name] = []

                gathered_metric_inputs[metric_name] += [batch_metric_inputs]

            if show_progress:
                self._write_to_stdout('>')

            return True

        if dataset is not None:
            for dataset_batch in dataset:
                success = gather_metrics_for(batch=dataset_batch)
                if not success:
                    return gathered_metric_inputs, success

        # By using two separate if-statements the IDE won't complain
        if model_outputs is not None:
            for model_output in model_outputs:
                success = gather_metrics_for(model_output=model_output)
                if not success:
                    return gathered_metric_inputs, success

        if show_progress:
            self._write_to_stdout('\n')

        return gathered_metric_inputs, True

    def combine_gathered_metric_inputs(self,
                                       gathered_metric_inputs,
                                       dataset_name=None,
                                       show_progress=None):
        """

        :param gathered_metric_inputs:
        :param dataset_name:
        :param show_progress:

        :return: combined_metric_inputs, success
        """
        dataset_desc = 'dataset' if dataset_name is None else f'{dataset_name} dataset'

        if show_progress is None:
            show_progress = self._show_progress

        if show_progress:
            metric_names = overlapping_metrics(self._combine_metric_inputs_funcs.keys(), gathered_metric_inputs.keys())
            self._log.debug(f"Combining gathered {dataset_desc} batch metric inputs "
                            f"(for metrics {', '.join(metric_names)})")

        combined_metric_inputs = {}
        success = True
        for metric_name, combine_func in self._combine_metric_inputs_funcs.items():
            if metric_name not in gathered_metric_inputs:
                continue

            try:
                metric_inputs_list = gathered_metric_inputs[metric_name]
                combined_metric_inputs[metric_name] = combine_func(metric_inputs_list)
            except Exception as e:
                _.log_exception(self._log, f"Combining gathered inputs for metric {metric_name} failed", e)
                success = False

        return combined_metric_inputs, success

    def calc_batch_metrics_for(self,
                               batch_data=None,
                               model_outputs: Optional[Union[Dict, BatchChunkingResults[Dict]]] = None,
                               evaluate_settings=None,
                               return_gathered_inputs=False):
        """

        Calculate metrics of given batch, optionally applying evaluate_settings

        :param batch_data:
        :type batch_data:

        :param model_outputs: Optional, externally calculated model outputs
                              (one model output for a single batch, or multiple outputs for multiple batch chunks)
        :type model_outputs: Union[Dict, BatchChunkingResults[Dict]]

        :param evaluate_settings:
        :type evaluate_settings:

        :param return_gathered_inputs: Optional, when True will also return the gathered inputs to
                                       calculate the metrics
        :param return_gathered_inputs: bool

        :return: Tuple[Dict, bool]
                    Dict {
                        "metrics": Dict with calculated metrics,
                        # Only if return_gathered_inputs:
                        "inputs": Dict with gathered inputs to calculate the metrics,
                    }

                    bool: success

        """
        results = {
            "metrics": None,
        }
        success = False

        if batch_data is not None and model_outputs is not None:
            self._log.error("Either provide a batch data or a list of model outputs, not both")
            return results, success

        evaluate_batch_in_chunks = isinstance(batch_data, ChunkableBatch) and self._batch_chunk_size is not None
        model_outputs_are_batch_chunking_results = isinstance(model_outputs, BatchChunkingResults)
        if evaluate_batch_in_chunks or model_outputs_are_batch_chunking_results:

            chunk_dataset = None
            if not model_outputs_are_batch_chunking_results:
                chunk_dataset = ChunkableBatchDataset(batch_data, self._batch_chunk_size)

            return self.calc_dataset_metrics_for(
                dataset=chunk_dataset,
                model_outputs=model_outputs,
                evaluate_settings=evaluate_settings,
                show_progress=False,
                return_gathered_inputs=return_gathered_inputs,
                dataset_name="batch chunks")

        # model_outputs is a single Dict
        gathered_inputs, success = self.gather_batch_metric_inputs(
            batch_data=batch_data,
            model_output=model_outputs,
            evaluate_settings=evaluate_settings)

        if return_gathered_inputs:
            results["inputs"] = gathered_inputs

        if not success:
            self._log.error(f"Gathering inputs to calculate batch metrics failed, stopping ...")
            return results, success

        metrics_output = {}
        success = True
        for metric_name, metric_func in self._metric_funcs.items():
            if metric_name not in gathered_inputs:
                continue

            try:
                metric_inputs = gathered_inputs[metric_name]
                metrics_output[metric_name] = self._eval_metric_func(
                    metric_func,
                    metric_inputs,
                    metric_name=metric_name)
            except Exception as e:
                _.log_exception(self._log, f"Evaluating metric {metric_name} over batch failed", e)
                success = False

        results["metrics"] = metrics_output

        return results, success

    def calc_metrics_using(self,
                           metric_inputs,
                           dataset_name=None,
                           show_progress=None):
        """

        Calculate metrics using a prepared set of metrics inputs

        :param metric_inputs: dict, with per metric (key) data to calculate metrics using the available `metric_funcs`
        :param dataset_name:
        :param show_progress:

        :return: (metric_outputs: dict, success: bool)
                  metric_output is dict with calculated metrics
        """
        dataset_desc = 'dataset' if dataset_name is None else f'{dataset_name} dataset'

        if show_progress is None:
            show_progress = self._show_progress

        if show_progress:
            metric_names = overlapping_metrics(self._metric_funcs.keys(), metric_inputs.keys())
            self._log.debug(f"Calculating metrics ({', '.join(metric_names)}) using data from the {dataset_desc}")

        metrics_output = {}
        success = True
        for metric_name, metric_func in self._metric_funcs.items():
            if metric_name not in metric_inputs:
                continue

            try:
                metrics_output[metric_name] = self._eval_metric_func(
                    metric_func,
                    metric_inputs[metric_name],
                    metric_name=metric_name)
            except Exception as e:
                _.log_exception(self._log, f"Evaluating metric {metric_name} using given metric inputs failed", e)
                success = False

        return metrics_output, success

    def calc_dataset_metrics_for(self,
                                 dataset: Optional[Iterable] = None,
                                 model_outputs: Optional[Iterable[Dict]] = None,
                                 evaluate_settings=None,
                                 dataset_name=None,
                                 show_progress=None,
                                 return_gathered_inputs=False):
        """
        Calculate metrics over whole dataset, by looping over the batches in the given dataset, optionally
        applying evaluate_settings

        :param dataset:
        :type dataset:

        :param model_outputs: Optional, externally calculated model outputs
                              This is used as an alternative to giving the dataset
        :type model_outputs: Optional[Iterable[Dict]]

        :param evaluate_settings:
        :type evaluate_settings:

        :param dataset_name:
        :type dataset_name:

        :param show_progress: Optional alternative value
        :type show_progress: bool

        :param return_gathered_inputs: Optional, when True will also return the gathered inputs to
                                       calculate the metrics
        :param return_gathered_inputs: bool

        :return Tuple[Dict, bool]
                Dict {
                        "metrics": Dict with calculated metrics,
                        # Only if return_gathered_inputs:
                        "inputs": Dict with gathered inputs to calculate the metrics,

                        "success": True if batch metric calculations were successful, else False
                     }

                bool: success
        """
        results = {
            "metrics": None,
        }
        success = False

        if dataset is not None and model_outputs is not None:
            self._log.error("Either provide a dataset or a list of model outputs, not both")
            return results, success

        dataset_desc = 'dataset' if dataset_name is None else f'{dataset_name} dataset'

        if show_progress is None:
            show_progress = self._show_progress

        if show_progress:
            metric_names = self.get_metric_names()
            self._log.debug(f"Calculating metrics ({', '.join(metric_names)}) over the {dataset_desc}")

        # ################## START: GATHER BATCH INPUTS OVER DATASET #####################
        gathered_inputs, success = self.gather_dataset_metric_inputs(
            dataset=dataset,
            model_outputs=model_outputs,
            evaluate_settings=evaluate_settings,
            dataset_name=dataset_name,
            show_progress=show_progress)

        if not success:
            self._log.error(f"Gathering of batch metric inputs over the {dataset_desc} failed, "
                            f"unable to calculate dataset metrics.")
            return results
        # #################### END: GATHER BATCH INPUTS OVER DATASET #####################

        # #################### START: COMBINE GATHERED BATCH INPUTS ######################
        gathered_inputs, success = self.combine_gathered_metric_inputs(
            gathered_inputs,
            dataset_name,
            show_progress)

        if return_gathered_inputs:
            results["inputs"] = gathered_inputs

        if not success:
            self._log.error(f"Combining of gathered batch metric inputs over the {dataset_desc} failed, "
                            f"unable to calculate dataset metrics.")
            return results, success
        # ###################### END: COMBINE GATHERED BATCH INPUTS #######################

        # ###################### START: CALCULATE DATASET METRICS #########################
        metrics_output, success = self.calc_metrics_using(gathered_inputs, dataset_name, show_progress)

        if not success:
            self._log.error(f"Evaluating metrics over the {dataset_desc} failed")
        # ####################### END: CALCULATE DATASET METRICS ##########################

        results["metrics"] = metrics_output

        return results, success

    def _create_chunkable_batch_dataset(self, batch_data) -> ChunkableBatchDatasetInterface:
        return convert_to_chunkable_dataset(
            batch_data,
            self._chunkable_batch_wrapper,
            self._batch_chunk_size
        )

    def _eval_metric_func(self, metric_func, metric_inputs, metric_name=None):
        # By default no special behavior
        return metric_func(metric_inputs)

    def _create_default_model_evaluate_func(self):
        """
        Creates function that evaluates model using the provided trainer instance.
        This needs to be implemented for any specific deep learning framework

        :return: The returned function has the following pattern:

                    f(batch, evaluate_settings) -> results

        :rtype: function (callable)
        """
        return lambda batch_data, settings: self._trainer.evaluate_loss(batch_data,
                                                                        inference_mode=True,
                                                                        evaluate_settings=settings)

    def _write_to_stdout(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def __str__(self):
        return self.get_name()

    @staticmethod
    def check_funcs(fdict, func_names=None):
        if is_empty(fdict) or not can_get_items(fdict):
            raise InvalidParametersException("A dict with one or more functions must be provided")

        if func_names is None:
            func_names = fdict.keys()

        for func_name in func_names:
            func = fdict[func_name]

            if not callable(func):
                raise InvalidParametersException(f"The function at {func_name} is not valid. "
                                                 f"The values of the function dictionary must be functions")

    @staticmethod
    def is_valid(ev):
        return has_method(ev, 'get_metric_names') and \
               has_method(ev, 'gather_batch_metric_inputs') and \
               has_method(ev, 'gather_dataset_metric_inputs') and \
               has_method(ev, 'combine_gathered_metric_inputs') and \
               has_method(ev, 'calc_batch_metrics_for') and \
               has_method(ev, 'calc_metrics_using') and \
               has_method(ev, 'calc_dataset_metrics_for')
