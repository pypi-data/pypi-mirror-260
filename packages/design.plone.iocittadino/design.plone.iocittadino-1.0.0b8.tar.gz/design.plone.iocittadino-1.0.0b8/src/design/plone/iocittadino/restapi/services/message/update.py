# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.interfaces import IMessageContentStore


# TODO; Make all the crud methods more generic
#   (this soup implementation seems to json rpc application crud archit. so can be used as ex.)
# also this method is not allowed, but we add it for a future development
@implementer(IPublishTraverse)
class UpdateRecord(Service):
    """Updates an existing record"""

    item_id = None

    def publishTraverse(self, request, name):
        if self.item_id is None:
            self.item_id = name
        return self

    def reply(self):
        if not self.item_id:
            return self.reply_no_content(status=404)

        data = json_body(self.request)
        portal = api.portal.getSite()
        adapter = queryMultiAdapter((portal, self.request), IMessageContentStore)
        try:
            res = adapter.update(self.item_id, data)
        except ValueError as e:
            raise BadRequest(str(e))
        except KeyError:
            return self.reply_no_content(status=404)
        if res:
            if res.get("error", "") == "NotFound":
                return self.reply_no_content(status=404)
            else:
                logger.error("Error updating record: {}".format(res))
                raise Exception(
                    translate(
                        _("generic_error_updating", "Error updating record."),
                        context=self.request,
                    )
                )
        # update success
        return self.reply_no_content()
