# -*- coding: utf-8 -*-
from urllib.request import urlopen

from plone import api
from plone.namedfile.file import NamedBlobFile
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.query import And
from repoze.catalog.query import Any
from repoze.catalog.query import Contains
from repoze.catalog.query import Eq
from repoze.catalog.query import Or
from souper.soup import Record
from souper.soup import get_soup
from zExceptions import NotFound
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.adapters.content_store import StoreRecord
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_MESSAGE
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_PRATICA
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_USER
from design.plone.iocittadino.data_store import DesignBaseDataStoreAdapterInterface
from design.plone.iocittadino.interfaces.store import IDesingBaseDataStore

from .blob_storage import BlobStorage


@implementer(IDesingBaseDataStore)
@adapter(Interface, Interface)
class DesignBaseDataStoreSoupAdapter(DesignBaseDataStoreAdapterInterface):
    """Storage imlementation by soup"""

    exception_messages = {
        NotFound: "The record with id:{id} was not found",
        ValueError: 'The value "{value}" is not valid',
    }
    content_type = None

    def __init__(self, context: object, request: object):
        self.context = context
        self.request = request
        self.portal = api.portal.get()

    @property
    def tempfile_storage(self):
        blob_storage_name = "desing.plone.iocittadino.tempfile_storage"
        portal_annotations = IAnnotations(api.portal.get())
        blob_storage = portal_annotations.get(blob_storage_name, None)

        if not blob_storage:
            portal_annotations[blob_storage_name] = BlobStorage()
            blob_storage = portal_annotations[blob_storage_name]

        return blob_storage

    def get_tempfile(self, fileid):
        return self.tempfile_storage.get(fileid)

    def add_tempfile(self, stream):
        return self.tempfile_storage.add(stream)

    def del_tempfile(self, fileid):
        if fileid in self.tempfile_storage:
            del self.tempfile_storage[fileid]

    @property
    def store(self):
        return get_soup(self.content_type, api.portal.get())

    @property
    def indexes(self):
        """
        Return all indexes in soup catalog
        """
        return [x for x in self.store.catalog.keys()]

    @property
    def keyword_indexes(self):
        """
        Return all keyword indexes in soup catalog
        """
        return [
            key
            for key, index in self.store.catalog.items()
            if isinstance(index, CatalogKeywordIndex)
        ]

    @property
    def text_indexes(self):
        return [
            key
            for key, index in self.store.catalog.items()
            if isinstance(index, CatalogTextIndex)
        ]

    @property
    def length(self) -> int:
        # TODO: find more efficent way to count the length, may be we need to check docs
        return len([x for x in self.store.data.values()])

    def add(self, object: dict) -> None:
        record = Record()

        self._manage_blob_fields(object)

        for key, val in object.items():
            # TODO: per renderlo più generico potrebbe essere definito
            # un tipo di campo in self.fields[key]
            if key == "attachments":
                attachments = []
                for elem in val or []:
                    blob = None
                    if elem.get("data"):
                        if elem["data"].startswith("data:"):
                            obj = urlopen(elem["data"])
                            data = obj.getvalue()
                            content_type = obj.headers.get("Content-Type")
                            blob = NamedBlobFile(
                                data=data,
                                contentType=content_type,
                                filename=elem.get("name"),
                            )
                    if blob:
                        attachments.append(
                            {
                                "name": elem["name"],
                                "blob": blob,
                                "type": content_type,
                                "size": len(data),
                            }
                        )
                    else:
                        logger.warning("wrong attachment %s" % elem)
                        attachments.append(elem)
                record.attrs[key] = attachments
            else:
                record.attrs[key] = val

        record_id = self.store.add(record)

        if not record_id:
            raise Exception(
                translate(
                    _(
                        "error_add_label",
                        default="Error creating a new record.",
                    ),
                    context=self.request,
                )
            )

        return self._compose_store_record(self.get(record_id))

    def get(self, item_id: int) -> StoreRecord:
        try:
            item_id = int(item_id)
        except ValueError:
            raise ValueError(self.exception_messages[ValueError].format(value=item_id))

        try:
            record = self.store.get(item_id)
        except KeyError:
            raise NotFound(self.exception_messages[NotFound].format(id=item_id))

        if not record:
            raise NotFound(self.exception_messages[NotFound].format(id=item_id))

        return self._compose_store_record(record)

    def update(self, item_id, validated_data) -> StoreRecord:
        """
        Update a form instance
        @param record: a StoreRecord with updated data
        @return update status (ok / no ok)
        """

        record = self.get(item_id)
        soup_record = self.store.get(record.intid)

        self._manage_blob_fields(form_data=validated_data)

        # XXX: 'data' is a special field, we need to handle it in a different way
        #       to avoid to overwrite the whole data field
        # XXX: attualmente per come è implementato update sovrascrive sempre
        #      tutto il contenuto.
        # if "data" in validated_data and "data" in soup_record.attrs:
        #     for key, val in validated_data["data"].items():
        #         soup_record.attrs["data"][key] = val
        #     del validated_data["data"]

        for k, v in validated_data.items():
            soup_record.attrs[k] = v

        self.store.reindex(records=[soup_record])

        return self._compose_store_record(soup_record)

    def delete(self, item_id: int) -> None:
        if not item_id:
            raise ValueError(
                translate(
                    _("missing_item_id", default="Missing record ID."),
                    context=self.request,
                )
            )

        record = self.get(item_id=item_id)

        if not record:
            raise NotFound(self.not_found_message.format(id=item_id))

        del self.store[record]

    def _manage_blob_fields(self, form_data):
        # Manage blob fields
        data = form_data.get("data", {})
        if type(data) is dict:
            for key, value in data.items():
                if type(value) is NamedBlobFile:
                    data[key] = {
                        "name": value.filename,
                        "blob": value,
                        "type": value.contentType,
                        "size": value.getSize(),
                    }

    def _parse_query_params(self, query={}):
        queries = []
        # force search only on user records if the user don't have a specific permission
        for index, value in query.items():
            if not value or value in ["*", "**"]:
                continue
            if index not in self.indexes:
                continue
            if index in self.text_indexes:
                queries.append(Contains(index, value))
            elif index in self.keyword_indexes:
                queries.append(Any(index, value))
            else:
                if isinstance(value, list):
                    queries.append(Or(*[Eq(index, x) for x in value]))
                else:
                    queries.append(Eq(index, value))
        if not queries:
            return None
        return And(*queries)

    def search(self, query: dict, sort_index: str, reverse: bool = True):
        parsed_query = self._parse_query_params(query=query)
        if parsed_query:
            results = self.store.query(
                queryobject=parsed_query,
                sort_index=sort_index,
                reverse=reverse,
            )
            return [self._compose_store_record(x) for x in results]
        # return all data
        records = self.store.data.values()
        if sort_index == "date":
            return sorted(
                [self._compose_store_record(i) for i in records],
                key=lambda k: k.attrs[sort_index] or None,
                reverse=reverse,
            )
        else:
            return sorted(
                [self._compose_store_record(i) for i in records],
                key=lambda k: k.attrs.get(sort_index, "") or "",
                reverse=reverse,
            )

    def clear(self) -> None:
        self.store.clear()

    def _compose_store_record(self, soup_record):
        return StoreRecord(
            intid=soup_record.intid,
            attrs=soup_record.attrs,
            type=self.content_type,
        )


class MessageDataStoreSoupAdapter(DesignBaseDataStoreSoupAdapter):
    content_type = CONTENT_TYPE_MESSAGE


class PraticaDataStoreSoupAdapter(DesignBaseDataStoreSoupAdapter):
    content_type = CONTENT_TYPE_PRATICA

    # Ovveride this to handle the pratica pdf report as a blob file
    def add(self, object: dict) -> None:
        for key, val in object.items():
            if key == "pratica_report":
                blob = None
                if type(val) is dict and val.get("data"):
                    if val["data"].startswith("data:"):
                        obj = urlopen(val["data"])
                        data = obj.getvalue()
                        content_type = obj.headers.get("Content-Type")
                        blob = NamedBlobFile(
                            data=data,
                            contentType=content_type,
                            filename=val.get("name"),
                        )
                if blob:
                    object[key] = {
                        "name": val["name"],
                        "blob": blob,
                        "type": content_type,
                        "size": len(data),
                    }
                else:
                    logger.warning("wrong pdf report %s" % val)

        return super().add(object)

    def update(self, item_id, validated_data) -> StoreRecord:
        """
        Update a form instance to handle the pratica report blob conversion
        @param record: a StoreRecord with updated data
        @return update status (ok / no ok)
        """
        for key, val in validated_data.items():
            if key == "pratica_report":
                blob = None
                if type(val) is dict and val.get("data"):
                    if val.get("data", "").startswith("data:"):
                        obj = urlopen(val["data"])
                        data = obj.getvalue()
                        content_type = obj.headers.get("Content-Type")
                        blob = NamedBlobFile(
                            data=data,
                            contentType=content_type,
                            filename=val.get("name"),
                        )
                if blob:
                    validated_data[key] = {
                        "name": val["name"],
                        "blob": blob,
                        "type": content_type,
                        "size": len(data),
                    }
                else:
                    logger.warning("wrong pdf report %s" % val)
                break

        return super().update(item_id, validated_data)


class UserDataStoreSoupAdapter(DesignBaseDataStoreSoupAdapter):
    content_type = CONTENT_TYPE_USER
