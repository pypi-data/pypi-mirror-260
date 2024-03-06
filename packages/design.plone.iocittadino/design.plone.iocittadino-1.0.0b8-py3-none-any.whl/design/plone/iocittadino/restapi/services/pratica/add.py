# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.interfaces import IUserStore


class AddRecord(Service):
    def reply(self):
        data = json_body(self.request)
        alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.getSite()
        store = queryMultiAdapter((portal, self.request), IPraticaContentStore)
        if "userid" in data:
            # remove given userid: can be fake
            del data["userid"]
        try:
            # XXX: store.add verifica anche che non esista già un record per lo
            #      stesso utente in fase di bozza o elaborazione
            record = store.add(data)
        except ValueError as e:
            raise BadRequest(str(e))

        # TODO: MAGARI DA SPOSTARE NEL METODO CHE SALVA LA PRATICA NEL TOOL
        user = api.user.get_current()
        userstore = queryMultiAdapter((self.context, user, self.request), IUserStore)
        userstore.set(data=data)

        return queryMultiAdapter((record, self.request), ISerializePraticaToJson)()
