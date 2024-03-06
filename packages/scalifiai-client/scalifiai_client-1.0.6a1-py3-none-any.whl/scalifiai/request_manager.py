from requests import request

from .constants import CREDENTIALS_AUTH_METHOD_API_KEY_KEY, AUTH_API_KEY_HEADER_NAME
from .exceptions import NotImplementedException


class RequestManager:
    # TODO[VIMPORTANT] CHECK AND MAKE FUNCTIONS PRIVATE IF THEY SHOULD NOT BE ACCESSIBLE DIRECTLY

    def __init__(self, *, credential_manager=None) -> None:
        self.credential_manager = credential_manager

    def add_request_auth(self, *, headers=None):

        if self.credential_manager.method == CREDENTIALS_AUTH_METHOD_API_KEY_KEY:
            headers = {
                **headers,
                AUTH_API_KEY_HEADER_NAME: self.credential_manager.api_key,
            }
        else:
            raise NotImplementedException()

        return headers

    def send_request(
        self,
        *,
        method=None,
        url=None,
        query_params=None,
        data=None,
        headers=None,
        files=None,
        stream=None
    ):

        if headers == None:
            headers = {}

        headers = self.add_request_auth(headers=headers)

        # TODO[VIMPORTANT] ADD CODE HERE TO HANDLE GENERIC ERRORS LIKE SUBSCRIPTION BASED, THROTTLING BASED, AUTHENTICATION, AUTHORIZATION AND BACKEND ERROR, REST CAN BE HANDLED EVERYWHERE ELSE

        return request(
            method=method,
            url=url,
            params=query_params,
            json=data,
            headers=headers,
            files=files,
            stream=stream,
        )
