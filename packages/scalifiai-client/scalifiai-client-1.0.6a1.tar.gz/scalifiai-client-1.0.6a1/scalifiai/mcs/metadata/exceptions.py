from scalifiai.exceptions import GeneralException


class MetadataException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata error: Unknown"


class MetadataNotFoundException(MetadataException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata error: Metadata not found"


class MetadataInvalidSimpleValueException(MetadataException):
    # TODO[VIMPORTANT] CONNECT THIS MESSAGE DIRECTLY TO THE SUPPORTED DATA TYPES THAT METADATA ACCEPTS, CAN BE ACCESSED VIA `type(value).__name__`, SEARCH IN CODE FOR MORE INFO
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata error: Invaid value, must be an int, float, or str."


class MetadataAlreadyExistsException(MetadataException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata error: Already exists"


# ---------------------------------------------------------------------------------------------


class MetadataProxyDictException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata Proxy Dict error: Unknown"


class MetadataProxyDictInvalidOperationValueException(MetadataProxyDictException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata Proxy Dict error: Invalid value for operation"


class MetadataProxyDictFindInvalidResponseException(MetadataProxyDictException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata Proxy Dict error: Invalid value to find metadata. Please contact our support team at helpdesk@scalifiai.com"


class MetadataProxyDictInvalidOperationException(MetadataProxyDictException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Metadata Proxy Dict error: Invalid operation"
