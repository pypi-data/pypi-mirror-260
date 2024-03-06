import pandas as pd
from typing import Any
from IPython.display import HTML
import humanize
from datetime import datetime

from scalifiai.base import BaseSubModule
from scalifiai.exceptions import BackendNotAvailableException, NotImplementedException
from scalifiai.mcs.main import MCS
from .constants import (
    URL_SLUG,
    COMPLETE_UPLOAD_URL_SLUG,
    GENERATE_DOWNLOAD_URL_URL_SLUG,
    DATA_TYPES_SIMPLE,
    DATA_TYPES_STORAGE,
)
from .exceptions import (
    MetadataNotFoundException,
    MetadataInvalidSimpleValueException,
    MetadataProxyDictInvalidOperationValueException,
    MetadataAlreadyExistsException,
    MetadataProxyDictFindInvalidResponseException,
    MetadataProxyDictInvalidOperationException,
)


class Metadata(BaseSubModule, MCS):
    # TODO[VIMPORTANT] CHECK AND MAKE FUNCTIONS PRIVATE IF THEY SHOULD NOT BE ACCESSIBLE DIRECTLY

    sub_module_url_slug = URL_SLUG

    complete_upload_url_slug = COMPLETE_UPLOAD_URL_SLUG
    generate_download_url_url_slug = GENERATE_DOWNLOAD_URL_URL_SLUG

    verbose_column_mapping = {
        "id": "ID",
        "created_at": "Created at",
        "updated_at": "Updated at",
        "uuid": "UUID",
        "delete_marker": "Marked for deletion",
        "properties__name": "Name",
        "properties__value": "Value",
        "properties__file_size": "Size",
        "data_type_verbose": "Data type",
        "key": "Full path",
    }

    instance_data = None

    # TODO[VIMPORTANT] ADD PYDANTIC SCHEMA FOR THIS
    def __init__(self, metadata_identifier=None, *, api_key=None) -> None:
        super().__init__(api_key=api_key)

        self.metadata_identifier = metadata_identifier

        data = self.retrieve()

        self.instance_data = data

    def __repr__(self):
        if self.instance_data["data_type"] in DATA_TYPES_SIMPLE:
            return f"Metadata(ID={self.instance_data['id']}, Key={self.instance_data['key']}, Value={self.instance_data['properties']['value']}, Data type={self.instance_data['data_type_verbose']})"
        elif self.instance_data["data_type"] in DATA_TYPES_STORAGE:
            return f"Metadata(ID={self.instance_data['id']}, Key={self.instance_data['key']}, Size={humanize.naturalsize(self.instance_data['properties']['file_size'])}, Data type={self.instance_data['data_type_verbose']})"
        else:
            raise NotImplementedException()

    # TODO[VIMPORTANT] ADD THIS PROPERTY TO ALL SUB-MODULES
    @property
    def info(self):

        html_content = "<table>"
        modified_instance_data = pd.json_normalize(
            self.instance_data, sep="__"
        ).to_dict(orient="records")[0]
        for key, value in modified_instance_data.items():
            final_key = (
                self.verbose_column_mapping.get(key, None)
                if self.verbose_column_mapping.get(key, None) != None
                else None
            )
            if final_key == None:
                continue

            final_value = value

            # TODO[VIMPORTANT] GENERALIZE THIS SO THAT WE CAN APPLY ANY FUNCTION TO ANY FIELDS BY SPECIFYINGIT IN THE VERBOSE COLUMNS CONFIG, CAN ALSO USE FUNCTIONS OF TABLE IN base.py
            if key in ["created_at", "updated_at"]:
                final_value = pd.to_datetime(final_value)
                if (datetime.now(self.local_timezone) - final_value).days > 0:
                    final_value = humanize.naturaldate(final_value)
                else:
                    final_value = humanize.naturaltime(final_value)

            # TODO[VIMPORTANT] GENERALIZE THIS SO THAT WE CAN APPLY ANY FUNCTION TO ANY FIELDS BY SPECIFYINGIT IN THE VERBOSE COLUMNS CONFIG, CAN ALSO USE FUNCTIONS OF TABLE IN base.py
            if key == "properties__file_size":
                final_value = humanize.naturalsize(final_value)

            html_content += f"<tr><th>{final_key}</th><td>{final_value}</td></tr>"
        html_content += "</table>"
        return HTML(html_content)

    # TODO[VIMPORTANT] ADD THIS PROPERTY TO ALL SUB-MODULES
    @property
    def raw_info(self):
        return self.instance_data

    def retrieve(self):

        url = self.generate_url(
            generic_action=True,
            resource_specific=True,
            resource_id=self.metadata_identifier,
        )

        # TODO[VIMPORTANT] ADD OPTION TO SEARCH 'ORG_WIDE' OR 'SELF_CREATED', SHOULD BE ACCESSIBLE IN ALL FUNCTIONS
        resp = self.request_manager.send_request(
            method="GET", url=url, query_params={"query_type": "SELF_CREATED"}
        )

        if resp.status_code == 200:
            return resp.json()["data"]
        elif resp.status_code == 404:
            raise MetadataNotFoundException()
        # TODO[VIMPORTANT] ADD CUSTOM EXCEPTIONS HERE TO HANDLE 400 RESPONSES
        else:
            raise BackendNotAvailableException()

    @classmethod
    def list(cls, *, extra_query_params=None, api_key=None):

        # TODO[VIMPORTANT] ADD CHECK HERE FOR CORRECT TYPE OF `extra_query_params`, THINK OF DOING IT VIA PYDANTIC AND ALSO FOR ALL OTHER FUNCTIONS
        if extra_query_params == None:
            extra_query_params = {}

        url = cls.generate_url(generic_action=True)

        # TODO[VIMPORTANT] ADD OPTION TO SEARCH 'ORG_WIDE' OR 'SELF_CREATED', SHOULD BE ACCESSIBLE IN ALL FUNCTIONS
        extra_query_params.update({"query_type": "SELF_CREATED"})
        request_manager = cls.get_request_manager(api_key=api_key)
        resp = request_manager.send_request(
            method="GET", url=url, query_params=extra_query_params
        )

        if resp.status_code == 200:
            return resp.json()["data"]
        # TODO[VIMPORTANT] ADD CUSTOM EXCEPTIONS HERE TO HANDLE 400 RESPONSES
        else:
            raise BackendNotAvailableException()

    def refresh_instance(self):

        data = self.retrieve()

        self.instance_data = data

    @classmethod
    def validate_and_return_data_type(cls, *, value=None):
        if not isinstance(value, (int, float, str)):
            raise MetadataInvalidSimpleValueException()
        return type(value).__name__


class MetadataProxyDict(dict):

    def __init__(
        self, *args, parent_instance=None, addition_auto_update=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.parent_instance = parent_instance
        self.addition_auto_update = addition_auto_update

    def set_addition_auto_update(self, value):

        if not isinstance(value, bool):
            raise MetadataProxyDictInvalidOperationValueException()

        self.addition_auto_update = value

    def __setitem__(self, __key, __value) -> None:

        data_type = Metadata.validate_and_return_data_type(value=__value)

        try:
            return self.parent_instance.add_metadata_simple(
                data_type=data_type, key=__key, value=__value
            )
        except MetadataAlreadyExistsException as ex:

            if self.addition_auto_update == True:

                # TODO[VIMPORTANT] REPLACE BELOW CODE WITH `self._getitem_internal` AS DONE IN `self.__getotem__`
                metadata_queryset = self.parent_instance._list_metadata(
                    extra_query_params={"key__exact": __key}
                )["results"]
                # TODO[VIMPORTANT] ADD A PYDANTIC CLASS HERE TO VERIFY THE RESPONSE STRUCTURE RETURNED

                print(f"metadata_queryset: {metadata_queryset}")

                if len(metadata_queryset) > 1:
                    raise MetadataProxyDictFindInvalidResponseException()
                elif len(metadata_queryset) == 1:
                    # TODO[VIMPORTANT] HANDLE THE CASE WHERE IF THE DATA TYPE OF ALREADY PRESENT INSTANCE IS NOT SIMPLE THEN IT SHOULD NOT UPDATE OF HANDLE THIS IN THE ERRORS OF `.update()` METHOD OF METDATA SUB-MODULE

                    self.parent_instance.update_metadata(
                        metadata_id=metadata_queryset[0]["id"],
                        data_type=data_type,
                        value=__value,
                    )

                    metadata_instance = Metadata(
                        metadata_queryset[0]["id"],
                        api_key=self.parent_instance.request_manager.credential_manager.api_key,
                    )
                    metadata_instance.refresh_instance()

                    return metadata_instance
                elif len(metadata_queryset) == 0:
                    return self.parent_instance.add_metadata_simple(
                        data_type=data_type, key=__key, value=__value
                    )

                return None

            raise ex

    def _getitem_internal(self, *, key=None):

        if isinstance(key, str) != True:
            raise MetadataProxyDictInvalidOperationValueException()

        metadata_queryset = self.parent_instance._list_metadata(
            extra_query_params={"key__exact": key}
        )["results"]

        # TODO[VIMPORTANT] ADD FILTER HERE TO NOT SHOW FILE TYPE METADATA OR THINK OF SOMETHING ELSE

        if len(metadata_queryset) > 1:
            raise MetadataProxyDictFindInvalidResponseException()
        elif len(metadata_queryset) == 1:
            metadata_instance = Metadata(
                metadata_queryset[0]["id"],
                api_key=self.parent_instance.request_manager.credential_manager.api_key,
            )

            return metadata_instance
        elif len(metadata_queryset) == 0:
            raise MetadataNotFoundException()

    def __getitem__(self, __key) -> Any:

        if isinstance(__key, str) != True:
            raise MetadataProxyDictInvalidOperationValueException()

        metadata_instance = self._getitem_internal(key=__key)
        return metadata_instance.instance_data["properties"]["value"]

    def __repr__(self):
        return repr(self.parent_instance.list_metadata())

    def upload_file(self, *, key=None, file_path=None):
        return self.parent_instance.add_metadata_storage(
            data_type="file", key=key, file_path=file_path
        )

    def __delitem__(self, __key: Any) -> None:

        metadata_instance = self._getitem_internal(key=__key)
        return self.parent_instance.delete_metadata(
            metadata_id=metadata_instance.instance_data["id"]
        )

    def popitem(self) -> tuple:
        raise MetadataProxyDictInvalidOperationException()

    def pop(self, __key):
        return self.__delitem__(__key)

    def clear(self):
        raise MetadataProxyDictInvalidOperationException()

    def items(self):
        raise MetadataProxyDictInvalidOperationException()
