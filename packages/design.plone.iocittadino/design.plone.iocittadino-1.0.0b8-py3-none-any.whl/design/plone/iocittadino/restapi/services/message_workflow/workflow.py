# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from design.plone.iocittadino.interfaces import IMessageContentStore


@implementer(IPublishTraverse)
class ChangeState(Service):
    """"""

    item_id = None

    def publishTraverse(self, request, name):
        if self.item_id is None:
            self.item_id = name
        return self

    def reply(self):
        if not self.item_id:
            return self.reply_no_content(status=400)
        data = json_body(self.request)
        adapter = queryMultiAdapter(
            (api.portal.get(), self.request), IMessageContentStore
        )
        if not data.get("state"):
            return self.reply_no_content(status=400)
        try:
            adapter.update_state(item_id=self.item_id, state=data["state"])
        except ValueError as e:
            raise BadRequest(str(e))
        except KeyError:
            return self.reply_no_content(status=404)
        # success
        return self.reply_no_content()
