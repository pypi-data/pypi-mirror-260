class ModelFrameworkException(Exception):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model framework error: Unknown"):
        self.message = message
        super().__init__(self.message)


class ModelFrameworkNoModelException(ModelFrameworkException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model framework error: No model provided"):
        self.message = message
        super().__init__(self.message)


class ModelFrameworkNotSupportedException(ModelFrameworkException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model framework error: Model framework not supported"):
        self.message = message
        super().__init__(self.message)


class ModelFrameworkNoKeyException(ModelFrameworkException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model framework error: No key provided"):
        self.message = message
        super().__init__(self.message)


class ModelWrapperException(Exception):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model wrapper error: Unknown"):
        self.message = message
        super().__init__(self.message)


class ModelWrapperInvalidModelException(Exception):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    def __init__(self, message="Model wrapper error: Invalid model"):
        self.message = message
        super().__init__(self.message)
