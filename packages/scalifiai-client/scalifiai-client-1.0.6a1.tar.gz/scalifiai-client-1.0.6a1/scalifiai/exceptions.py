class GeneralException(Exception):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "General error: Unknown"

    def __init__(self, *, message=None, internal_data=None):
        if message == None:
            self.message = self.default_message
        else:
            self.message = message

        self.internal_data = internal_data

        super().__init__(self.message)


class NotImplementedException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "General error: Not implemented"


class BackendNotAvailableException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Backend error: Experiencing some issues, please try again."


class QuotaException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Quota error: Unknown"


class QuotaExceededException(QuotaException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Quota error: Quota expired"


# ---------------------------------------------------------------------------------------------


class CredentialException(GeneralException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Credentials error: Unknown"


class CredentialAPIKeyMissingException(CredentialException):
    # TODO[VIMPORTANT] ADD PROPER MESSAGE WITH INSTRUCTIONS
    default_message = "Credentials error: API key not found"


# ---------------------------------------------------------------------------------------------


def raise_general_exception(*, response=None, internal_data=None):

    try:
        data = response.json()
    except Exception:
        raise BackendNotAvailableException(internal_data=internal_data)

    key_data = data["error_codes"]
    if key_data.get("status", None) != None:
        if key_data["status"] == "quota_exceeded":
            if data.get("detail", None) != None:
                raise QuotaExceededException(
                    message=data["detail"], internal_data=internal_data
                )
            raise QuotaExceededException(internal_data=internal_data)
