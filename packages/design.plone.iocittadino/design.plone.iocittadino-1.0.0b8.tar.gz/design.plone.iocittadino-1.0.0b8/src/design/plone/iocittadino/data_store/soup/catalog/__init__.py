# -*- coding: utf-8 -*-
"""This module is not generic and must be impemented manualy if migrate to an other storage"""
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.soup import NodeAttributeIndexer


class SoupCatalogFactory:
    """Base catalog factory for a souper storage"""

    def __call__(self, *args, **kwargs):
        catalog = Catalog()

        userid_indexer = NodeAttributeIndexer("userid")
        catalog["userid"] = CatalogFieldIndex(userid_indexer)

        return catalog
