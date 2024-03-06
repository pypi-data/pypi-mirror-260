# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.component import queryMultiAdapter

# from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

# from design.plone.iocittadino import _
# from design.plone.iocittadino import logger
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.interfaces import IUserStore


@implementer(IPublishTraverse)
class UpdateRecord(Service):
    """Updates an existing record"""

    item_id = None

    def publishTraverse(self, request, name):
        if self.item_id is None:
            self.item_id = name
        return self

    def reply(self):
        if self.item_id is None:
            return self.reply_no_content(status=404)
        alsoProvides(self.request, IDisableCSRFProtection)
        data = json_body(self.request)
        store = queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        )
        try:
            # XXX: update fa verifiche sul fatto che sis sta aggiornando
            #      una pratica non in bozza ?
            record = store.update(item_id=self.item_id, data=data)
        except ValueError as e:
            raise BadRequest(str(e))
        except KeyError:
            return self.reply_no_content(status=404)
        except NotFound:
            return self.reply_no_content(status=404)

        # TODO: MAGARI DA SPOSTARE NEL METODO CHE SALVA LA PRATICA NEL TOOL
        user = api.user.get_current()
        userstore = queryMultiAdapter((self.context, user, self.request), IUserStore)
        userstore.set(data=data)

        # except Exception as e:
        #     logger.error("Error updating record: {}".format(e))
        #     raise Exception(
        #         translate(
        #             _("generic_error_updating", "Error updating record."),
        #             context=self.request,
        #         )
        #     )
        # if not record:
        #     if res.get("error", "") == "NotFound":
        #         return self.reply_no_content(status=404)
        #     else:
        #         logger.error("Error updating record: {}".format(res))
        #         raise Exception(
        #             translate(
        #                 _("generic_error_updating", "Error updating record."),
        #                 context=self.request,
        #             )
        #         )
        return queryMultiAdapter((record, self.request), ISerializePraticaToJson)()
