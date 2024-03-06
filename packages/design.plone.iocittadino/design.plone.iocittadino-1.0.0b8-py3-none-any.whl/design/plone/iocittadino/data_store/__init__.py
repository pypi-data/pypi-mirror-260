# -*- coding: utf-8 -*-
from typing import List


class StoreRecord:
    """Storage obj class

    Attributes:
        attrs (dict): Dictionary with the record values
        type (str): Type of the record
        intid (int): Unique id of the record in his storage namespace
    """

    def __init__(self, intid: int, attrs: dict, type: str) -> None:
        # those attributes provide backward compatibility with the code
        # written before in the tight coupling with a
        # soup storage
        self.type = type
        self.intid = intid
        self.attrs = attrs

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return "%s object at %s type:%s, id:%d" % (
            self.__class__,
            hex(id(self)),
            self.type,
            self.intid,
        )


class DesignBaseDataStoreAdapterInterface:
    """Basic implementation of the store adapter"""

    @property
    def exception_messages(self) -> dict:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    @property
    def content_type(self) -> str:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    @property
    def store(self) -> object:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    @property
    def indexes(self) -> List[str]:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    @property
    def text_indexes(self) -> List[str]:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    @property
    def keyword_indexes(self) -> List[str]:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def add(self, item_id: int) -> StoreRecord:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def update(self, item_id: int, validated_data: dict) -> StoreRecord:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def get(self, item_id: int) -> StoreRecord:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def delete(self, item_id: int) -> StoreRecord:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def search(
        self, query: dict, sort_index: str, reverse: bool = True
    ) -> List[StoreRecord]:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def length(self) -> int:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def clear(self) -> None:
        """Method which deletes all the storage entries"""
        raise NotImplementedError("The method was not implemented")  # pragma: no cover

    def _compose_store_record(self, record: None) -> StoreRecord:
        raise NotImplementedError("The method was not implemented")  # pragma: no cover
