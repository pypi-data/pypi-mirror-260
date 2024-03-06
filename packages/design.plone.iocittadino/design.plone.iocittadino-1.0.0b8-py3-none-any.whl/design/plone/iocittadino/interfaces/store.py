# -*- coding: utf-8 -*-
from zope.interface import Interface


class ISerializePraticheToJson(Interface):
    """
    Serializer for a list of pratiche
    """


class ISerializePraticaToJson(Interface):
    """
    Serializer for a pratica
    """


class ISerializePraticaToJsonSummary(Interface):
    """
    Summary Serializer for a pratica
    """


class ISerializeMessageToJson(Interface):
    """
    Serializer for a message
    """


class ISerializeMessageToJsonSummary(Interface):
    """
    Summary serializer for a message
    """


class ISerializeMessagesToJson(Interface):
    """
    Serializer for a list of messages
    """


class IUserStore(Interface):
    def __init__(context, user, request):
        """
        Adapts a user
        """

    def get():
        """
        Return all the values for a user
        """

    def set(kwargs):
        """
        Store user data
        """


class IDesingBaseDataStore(Interface):
    """Interface for CRUD storage"""

    def get(item_id):
        """
        @param item_id: The int id of an existing item
        @return: Existing object with givent id or NotFound
        """

    def add(data):
        """
        @param data: Dictionary with new item data
        @return: ok / no ok
        """

    def update(item_id, data):
        """
        @param item_id: The int id of an existing item
        @param data: Dictionary with data to update
        @return: ok / no ok
        """

    def delete(item_id):
        """
        @param item_id: The int id of an existing item
        @return: ok /no ok
        """

    def search(query, sort_index, reverse):
        """
        @param query: Dictionary with searching params
        @param sort_index: Sorting index
        @param reverse: Bool
        @return: List of found items or an empty list
        """

    def length():
        """
        @return: Int current lenght of the of the storage
        """

    def add_tempfile(stream):
        """
        Store a temporary file

        @param stream: File stream

        @return: String fileid
        """

    def get_tempfile(fileid):
        """
        Get a temporary file

        @param fileid: String fileid

        @return: Blob / File stream
        """

    def del_tempfile(fileid):
        """
        Delete a temporary file

        @param fileid: String fileid

        @return: ok / no ok
        """

    def _compose_store_record(self, record):
        """Compose StoreRecord object form the storage record item
        @return: StoreRecord object
        """


class IPraticaContentStore(Interface):
    """
    Interface for Store adapters. Each adapter should implement these methods
    """

    def __init__(context, request):
        """
        Adapts context and request
        """

    def get_records_by_form_id(form_id):
        """
        Return all records for a form; useful to get all the pratica
        @param form_id: a form id
        @return: the list of form instance related to a specific form/service
        """


class IPraticaStoreFieldsExtender(Interface):
    """
    Interface for Store adapters; we can use it to mark utilities that provides
    fields to extend the default ones
    """


class IPraticaStoreSerializerExtender(Interface):
    """
    Interface for Pratica Store serializer; we can use it to mark utilities that
    provides metadata to extend the default serializer
    """


class IMessageStoreFieldsExtender(Interface):
    """
    Interface for Store adapters; we can use it to mark utilities that provides
    fields to extend the default ones
    """


class IMessageStoreSerializerExtender(Interface):
    """
    Interface for Message Store serializer; we can use it to mark utilities that
    provides metadata to extend the default serializer
    """


class IMessageContentStore(Interface):
    """
    Interface for Store adapters. Each adapter should implement these methods
    """

    def __init__(context, request):
        """
        Adapts context and request
        """

    def get_record_by_pratica_id(pratica_id):
        """
        Return a record by it's id
        @param pratica_id: a record (form instance) id
        @return: all data related to a specific record
        """
