from scalifiai.exceptions import GeneralException


class MCSSubModuleTagsProxyDictException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Tags Proxy Dict error: Unknown"


class MCSSubModuleTagsProxyDictInvalidOperationValueException(
    MCSSubModuleTagsProxyDictException
):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Tags Proxy Dict error: Invalid value for operation"


class MCSSubModuleTagsProxyDictFindInvalidResponseException(
    MCSSubModuleTagsProxyDictException
):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Tags Proxy Dict error: Invalid value to find tag. Please contact our support team at helpdesk@scalifiai.com"


class MCSSubModuleTagsProxyDictInvalidOperationException(
    MCSSubModuleTagsProxyDictException
):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Tags Proxy Dict error: Invalid operation"
