
class MLPugException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message} :\n\n{self.__cause__}"


class CallbackInvalidException(MLPugException):
    def __init__(self, callback_name, message=None):
        err_msg = f"Callback {callback_name} is invalid"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class CallbackBadUseException(MLPugException):
    def __init__(self, callback_name, message=None):
        err_msg = f"Bad use of Callback {callback_name}"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class TrainerInvalidException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Trainer is invalid"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class TrainerStateInvalidException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Trainer state is invalid"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class BatchNotChunkableException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Given batch is not chunkable, provide a `chunkable_batch_wrapper` to make your match chunkable, or" \
                  "ensure that the batch object is derived from the `ChunkableBatch` class"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class StateInvalidException(MLPugException):
    def __init__(self, message=None):
        err_msg = "State invalid, unable to set state"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class InvalidParametersException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Invalid parameter(s)"
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class LossNotAvailableException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Key 'loss' not available in evaluation results dict. " \
                  "TIP : your model needs to return a dict with a 'loss' key."
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)


class NumSamplesNotAvailableException(MLPugException):
    def __init__(self, message=None):
        err_msg = "Key 'num_samples' not available in evaluation results dict. " \
                  "TIP : your model needs to return a dict with a 'num_samples' key."
        if message:
            err_msg += f" : {message}"

        super().__init__(err_msg)
