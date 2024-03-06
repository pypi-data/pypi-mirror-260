# -*- coding: utf-8 -*-
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer

from design.plone.iocittadino.data_store.soup.catalog import SoupCatalogFactory


@implementer(ICatalogFactory)
class MessageSoupCatalogFactory(SoupCatalogFactory):
    def __call__(self, context, *args, **kwargs):
        catalog = super().__call__(context=context, *args, **kwargs)

        title = NodeAttributeIndexer("title")
        catalog["title"] = CatalogFieldIndex(title)
        catalog["date"] = CatalogFieldIndex(NodeAttributeIndexer("date"))
        pratica_id_indexer = NodeAttributeIndexer("pratica_id")
        catalog["pratica_id"] = CatalogFieldIndex(pratica_id_indexer)
        object_uid_indexer = NodeAttributeIndexer("object_uid")
        catalog["object_uid"] = CatalogFieldIndex(object_uid_indexer)
        messageid_indexer = NodeAttributeIndexer("messageid")
        catalog["messageid"] = CatalogFieldIndex(messageid_indexer)
        state_indexer = NodeAttributeIndexer("state")
        catalog["state"] = CatalogFieldIndex(state_indexer)
        email_indexer = NodeAttributeIndexer("email")
        catalog["email"] = CatalogFieldIndex(email_indexer)

        return catalog
