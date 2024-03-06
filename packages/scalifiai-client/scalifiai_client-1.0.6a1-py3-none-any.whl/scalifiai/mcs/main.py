from scalifiai.base import BaseModule
from scalifiai.mcs.model.exceptions import ModelTagNotFoundException
from .constants import URL_SLUG
from .exceptions import (
    MCSSubModuleTagsProxyDictInvalidOperationValueException,
    MCSSubModuleTagsProxyDictFindInvalidResponseException,
    MCSSubModuleTagsProxyDictInvalidOperationException,
)


class MCS(BaseModule):
    # TODO[VIMPORTANT] CHECK AND MAKE FUNCTIONS PRIVATE IF THEY SHOULD NOT BE ACCESSIBLE DIRECTLY

    module_url_slug = URL_SLUG


class MCSSubModuleTagsProxyDict(dict):

    def __init__(self, *args, parent_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_instance = parent_instance

    def __setitem__(self, __key, __value) -> None:

        return self.parent_instance.attach_tags(tags=[{"key": __key, "value": __value}])

    def _getitem_internal(self, *, key=None):

        if isinstance(key, str) != True:
            raise MCSSubModuleTagsProxyDictInvalidOperationValueException()

        tags_queryset = self.parent_instance._list_tags(
            extra_query_params={"key__exact": key}
        )["results"]

        # TODO[VIMPORTANT] ADD FILTER HERE TO NOT SHOW FILE TYPE METADATA OR THINK OF SOMETHING ELSE

        if len(tags_queryset) > 1:
            raise MCSSubModuleTagsProxyDictFindInvalidResponseException()
        elif len(tags_queryset) == 1:

            return tags_queryset[0]
        elif len(tags_queryset) == 0:
            raise ModelTagNotFoundException()

    def __getitem__(self, __key):

        if isinstance(__key, str) != True:
            raise MCSSubModuleTagsProxyDictInvalidOperationValueException()

        tag_data = self._getitem_internal(key=__key)
        return tag_data["value"]

    def __repr__(self):
        return repr(self.parent_instance.list_tags())

    def __delitem__(self, __key) -> None:

        tag_data = self._getitem_internal(key=__key)
        return self.parent_instance.remove_tag(tag_id=tag_data["id"])

    def popitem(self) -> tuple:
        raise MCSSubModuleTagsProxyDictInvalidOperationException()

    def pop(self, __key):
        return self.__delitem__(__key)

    def clear(self):
        return self.parent_instance.remove_all_tags()

    def items(self):
        raise MCSSubModuleTagsProxyDictInvalidOperationException()
