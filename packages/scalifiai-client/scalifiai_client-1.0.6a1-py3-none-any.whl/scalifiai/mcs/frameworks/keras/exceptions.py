from scalifiai.exceptions import GeneralException


class KerasModelWrapperException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Keras model wrapper error: Unknown"


class KerasInvalidDataTypeModelException(KerasModelWrapperException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Keras model wrapper error: Invalid data type"


class KerasInvalidModelException(KerasModelWrapperException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Keras model wrapper error: Invalid model"
