# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from zope.interface import implementer

from design.plone.iocittadino.interfaces import IModelloPratica


@implementer(IModelloPratica)
class ModelloPratica(Item):
    """Content-type class for IModelloPratica"""
