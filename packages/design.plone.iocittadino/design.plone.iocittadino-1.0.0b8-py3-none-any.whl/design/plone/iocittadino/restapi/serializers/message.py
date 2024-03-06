# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import datetimelike_to_iso
from zExceptions import NotFound
from zope import component
from zope import interface
from zope.component import queryMultiAdapter
from zope.component import getAllUtilitiesRegisteredFor
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import ISerializeMessagesToJson
from design.plone.iocittadino.interfaces import ISerializeMessageToJson
from design.plone.iocittadino.interfaces import ISerializeMessageToJsonSummary
from design.plone.iocittadino.interfaces import ISerializePraticaToJsonSummary
from design.plone.iocittadino.interfaces.store import IMessageStoreSerializerExtender

from .mixin import PortalUrlMixIn


class MessageAttachmentsMixIn(PortalUrlMixIn):
    message = None

    def __call__(self, *args, **kwargs):
        return {
            "attachments": self.get_attachments(),
        }

    def get_attachments(self):
        result = []

        root_url = self.get_portal_url()

        for idx, attachment in enumerate(self.message.attrs.get("attachments") or []):
            filename = attachment.get("name", "file")
            result.append(
                {
                    "name": filename,
                    "url": f"{root_url}/message/{self.message.intid}/@@download/{idx}/{filename}",
                }
            )
        return result


@interface.implementer(ISerializeMessageToJson)
@component.adapter(interface.Interface, interface.Interface)
class MessageSerializer(MessageAttachmentsMixIn):
    def __init__(self, message, request):
        self.message = message
        self.request = request

    def __call__(self, *args, **kwargs):
        result = {
            **super().__call__(*args, **kwargs),
            "item_id": self.message.intid,
            "title": self.message.attrs.get("title"),
            "userid": self.message.attrs.get("userid"),
            "state": self.message.attrs.get("state"),
            "date": datetimelike_to_iso(self.message.attrs.get("date")),
            "message": self.message.attrs.get("message"),
            # probabilmente questi due campi potrebbero collassare in uno solo
            "pratica": self.get_pratica_summary(),
            "object": self.get_object_summary(),
        }
        for utility in getAllUtilitiesRegisteredFor(IMessageStoreSerializerExtender):
            result.update(utility.get_fields(self.message))
        return result

    def get_pratica_summary(self):
        pratica_id = self.message.attrs.get("pratica_id", "")
        if not pratica_id:
            return None
        try:
            pratica = queryMultiAdapter(
                (api.portal.get(), self.request), IPraticaContentStore
            ).get(pratica_id)
        except NotFound:
            return None
        if not pratica:
            return None
        try:
            return component.getMultiAdapter(
                (pratica, self.request), ISerializePraticaToJsonSummary
            )()
        except Unauthorized:
            return None

    def get_object_summary(self):
        object_uid = self.message.attrs.get("object_uid", "")

        if not object_uid:
            return None

        obj = api.content.get(UID=object_uid)

        if not obj:
            return None

        return component.getMultiAdapter((obj, self.request), ISerializeToJson)()


@interface.implementer(ISerializeMessageToJsonSummary)
@component.adapter(interface.Interface, interface.Interface)
class MessageSummarySerializer(MessageAttachmentsMixIn):
    def __init__(self, message, request):
        self.message = message
        self.request = request

    def __call__(self, *args, **kwargs):
        result = {
            **super().__call__(*args, **kwargs),
            "item_id": self.message.intid,
            "title": self.message.attrs.get("title"),
            "userid": self.message.attrs.get("userid"),
            "state": self.message.attrs.get("state"),
            "date": datetimelike_to_iso(self.message.attrs.get("date")),
            "message": self.message.attrs.get("message"),
        }
        return result


@interface.implementer(ISerializeMessagesToJson)
@component.adapter(list, interface.Interface)
class MessageListSerializer:
    def __init__(self, messages, request):
        self.messages = messages
        self.request = request

    def __call__(self):
        results = {}
        results["items_total"] = len(self.messages)
        results["items"] = []
        for message in self.messages:
            result = component.getMultiAdapter(
                (message, self.request), ISerializeMessagesToJson
            )()
            results["items"].append(result)
        return results
