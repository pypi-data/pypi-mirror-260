# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.interfaces import IMessageContentStore


@implementer(IPublishTraverse)
class DeleteRecord(Service):
    """Deletes a content object."""

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        self.params.append(name)
        return self

    def reply(self):
        if not self.params:
            return self.reply_no_content(status=404)
        portal = api.portal.getSite()
        adapter = queryMultiAdapter((portal, self.request), IMessageContentStore)

        try:
            res = adapter.delete(item_id=int(self.params[0]))
        except ValueError as e:
            raise BadRequest(str(e))

        if res:
            if res.get("error", "") == "NotFound":
                return self.reply_no_content(status=404)
            else:
                logger.error("Error deleting record: {}".format(res))
                raise Exception(
                    translate(
                        _("generic_error_deleting", "Error deleting record."),
                        context=self.request,
                    )
                )

        return self.reply_no_content()
