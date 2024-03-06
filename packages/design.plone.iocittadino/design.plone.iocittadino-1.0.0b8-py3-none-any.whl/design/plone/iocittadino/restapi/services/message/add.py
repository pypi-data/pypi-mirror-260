# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

from design.plone.iocittadino.interfaces import IMessageContentStore


class AddRecord(Service):
    def reply(self):
        data = json_body(self.request)
        alsoProvides(self.request, IDisableCSRFProtection)

        portal = api.portal.getSite()
        adapter = queryMultiAdapter((portal, self.request), IMessageContentStore)
        if "userid" in data:
            # remove given userid: can be fake
            del data["userid"]
        try:
            message = adapter.add(data)
        except ValueError as e:
            raise BadRequest(str(e))
        return {"item_id": message.intid}
