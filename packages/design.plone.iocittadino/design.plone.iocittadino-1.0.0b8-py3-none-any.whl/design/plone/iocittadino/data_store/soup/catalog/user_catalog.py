# -*- coding: utf-8 -*-
from souper.interfaces import ICatalogFactory
from zope.interface import implementer

from design.plone.iocittadino.data_store.soup.catalog import SoupCatalogFactory


@implementer(ICatalogFactory)
class UserSoupCatalogFactory(SoupCatalogFactory):
    pass
