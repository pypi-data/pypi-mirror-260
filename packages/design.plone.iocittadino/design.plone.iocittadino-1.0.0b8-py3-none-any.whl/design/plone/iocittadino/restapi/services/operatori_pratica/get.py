# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.batching import HypermediaBatch
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from design.plone.iocittadino import logger


@implementer(IPublishTraverse)
class GetOperatori(Service):
    """
    Get single record
    """

    def reply(self):
        """ """
        try:
            members = [
                {
                    "value": x.getId(),
                    "label": x.getProperty("fullname", x.getId()),
                }
                for x in api.user.get_users(groupname="operatori_pratiche")
            ]
        except api.exc.GroupNotFoundError:
            logger.error("Group operatori_pratiche not found")
            members = [{"value": "admin", "label": "admin"}]
        members = sorted(members, key=lambda x: x["value"])
        batch = HypermediaBatch(self.request, members)
        data = {}
        data["items"] = [x for x in batch]
        data["items_total"] = batch.items_total
        links = batch.links
        if links:
            data["batching"] = links
        return data
