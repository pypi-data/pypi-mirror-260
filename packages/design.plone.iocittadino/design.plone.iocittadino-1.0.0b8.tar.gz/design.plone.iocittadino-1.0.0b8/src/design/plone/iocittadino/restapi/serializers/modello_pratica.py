# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson as BaseSerializer
from zExceptions import Unauthorized
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino.interfaces import IModelloPratica


@implementer(ISerializeToJson)
@adapter(IModelloPratica, Interface)
class SerializeToJson(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        if not api.user.has_permission("design.plone.iocittadino: CRUD Pratica"):
            raise Unauthorized("You need to log-in to access this content.")
        return super().__call__(version=version, include_items=include_items)
