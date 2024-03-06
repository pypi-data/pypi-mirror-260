# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer

from design.plone.iocittadino.content.modello_pratica import IModelloPratica


@indexer(IModelloPratica)
def tassonomia_argomenti(context, **kw):
    return [
        x.to_object.Title()
        for x in getattr(context.aq_parent.aq_base, "tassonomia_argomenti", [])
        if x.to_object
    ]
