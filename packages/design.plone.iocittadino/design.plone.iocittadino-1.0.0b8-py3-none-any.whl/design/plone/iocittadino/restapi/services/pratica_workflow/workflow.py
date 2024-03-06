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


@implementer(IPublishTraverse)
class ChangeState(Service):
    """Change state of a pratica"""

    item_id = None

    def publishTraverse(self, request, name):
        if self.item_id is None:
            self.item_id = name
        return self

    def reply(self):
        if not self.item_id:
            return self.reply_no_content(status=404)
        alsoProvides(self.request, IDisableCSRFProtection)
        data = json_body(self.request)
        portal = api.portal.getSite()
        adapter = queryMultiAdapter((portal, self.request), IPraticaContentStore)

        try:
            adapter.update_state(item_id=self.item_id, state=data.get("state", ""))
        except ValueError as e:
            raise BadRequest(str(e))
        except KeyError:
            return self.reply_no_content(status=404)
        except NotFound:
            return self.reply_no_content(status=404)
        # if res:
        #     if res.get("error", "") == "NotFound":
        #         return self.reply_no_content(status=404)
        #     else:
        #         logger.error("Error updating record state: {}".format(res))
        #         raise Exception(
        #             translate(
        #                 _("generic_error_updating_wf", "Error updating record state."),
        #                 context=self.request,
        #             )
        #         )
        # update success
        return self.reply_no_content()
