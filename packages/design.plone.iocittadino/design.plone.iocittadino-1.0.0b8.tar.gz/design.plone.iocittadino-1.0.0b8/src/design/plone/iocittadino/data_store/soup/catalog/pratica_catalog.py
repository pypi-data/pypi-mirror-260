# -*- coding: utf-8 -*-
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer

from design.plone.iocittadino.data_store.soup.catalog import SoupCatalogFactory


@implementer(ICatalogFactory)
class PraticaSoupCatalogFactory(SoupCatalogFactory):
    def __call__(self, context, *args, **kwargs):
        catalog = super().__call__(context=context, *args, **kwargs)

        form_id_indexer = NodeAttributeIndexer("form_id")
        catalog["form_id"] = CatalogFieldIndex(form_id_indexer)

        state_indexer = NodeAttributeIndexer("state")
        catalog["state"] = CatalogFieldIndex(state_indexer)

        # creation_date
        catalog["date"] = CatalogFieldIndex(NodeAttributeIndexer("date"))
        catalog["modification_date"] = CatalogFieldIndex(
            NodeAttributeIndexer("modification_date")
        )

        numero_protocollo_indexer = NodeAttributeIndexer("numero_protocollo")
        catalog["numero_protocollo"] = CatalogFieldIndex(numero_protocollo_indexer)

        servizio_indexer = NodeAttributeIndexer("servizio")
        catalog["servizio"] = CatalogFieldIndex(servizio_indexer)

        ufficio_indexer = NodeAttributeIndexer("ufficio")
        catalog["ufficio"] = CatalogKeywordIndex(ufficio_indexer)

        ongoing_date = NodeAttributeIndexer("ongoing_date")
        catalog["ongoing_date"] = CatalogFieldIndex(ongoing_date)

        email = NodeAttributeIndexer("email")
        catalog["email"] = CatalogFieldIndex(email)

        assigned_to = NodeAttributeIndexer("assigned_to")
        catalog["assigned_to"] = CatalogFieldIndex(assigned_to)

        return catalog
