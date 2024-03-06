from scalifiai.exceptions import (
    raise_general_exception,
    GeneralException,
    BackendNotAvailableException,
)
from scalifiai.mcs.metadata.exceptions import MetadataAlreadyExistsException


class ModelVersionException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model version error: Unknown"


class ModelVersionNotFoundException(ModelVersionException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model version error: Model version not found"


class ModelVersionModelFetchException(ModelVersionException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model version error: Error fetching model file"


class ModelVersionAddMetadataSimpleException(ModelVersionException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Model version error: Error adding simple metadata"


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
        if data["error_codes"].get("non_field_errors", None) != None:
            key_data = data["error_codes"]
        else:
            key_data = data["error_codes"]["metadata"]
        if key_data.get("non_field_errors", None) != None:
            if key_data["non_field_errors"][0] == "unique":
                raise MetadataAlreadyExistsException(internal_data=internal_data)
            elif key_data["non_field_errors"][0] == "invalid":
                error_message = f"{ModelVersionAddMetadataSimpleException.default_message}\nError:\n{data['non_field_errors'][0]}"
                raise ModelVersionAddMetadataSimpleException(
                    internal_data=internal_data, message=error_message
                )
            else:
                raise BackendNotAvailableException(internal_data=internal_data)
        else:
            raise BackendNotAvailableException(internal_data=internal_data)
    else:
        raise BackendNotAvailableException(internal_data=internal_data)
