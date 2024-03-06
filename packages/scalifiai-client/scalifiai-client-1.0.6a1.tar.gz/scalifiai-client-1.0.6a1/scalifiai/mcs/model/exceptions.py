from scalifiai.exceptions import (
    raise_general_exception,
    GeneralException,
    BackendNotAvailableException,
)
from scalifiai.mcs.metadata.exceptions import MetadataAlreadyExistsException


class ModelException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model error: Unknown"


class ModelNotFoundException(ModelException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model error: Model not found"


class ModelTagNotFoundException(ModelException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model error: Tag not found"


def raise_custom_exception(
    *, response=None, action=None, func_name=None, internal_data=None
):

    raise_general_exception(response=response, internal_data=internal_data)

    main_key = None

    if action != None and func_name != None:
        raise Exception("Cannot provide both `action` and `func_name` together")

    if action != None:
        main_key = action

    if func_name != None:
        main_key = func_name

    if main_key == None:
        raise Exception(f"Invalid main_key value: {main_key}")

    try:
        data = response.json()
    except Exception:
        raise BackendNotAvailableException(internal_data=internal_data)

    if data.get("error_codes", None) == None:
        raise BackendNotAvailableException(internal_data=internal_data)

    if main_key == "add_metadata_simple":
        key_data = data["error_codes"]["metadata"]
        if key_data.get("non_field_errors", None) != None:
            if key_data["non_field_errors"][0] == "unique":
                raise MetadataAlreadyExistsException(internal_data=internal_data)
            else:
                raise BackendNotAvailableException(internal_data=internal_data)
        else:
            raise BackendNotAvailableException(internal_data=internal_data)
    else:
        raise BackendNotAvailableException(internal_data=internal_data)
