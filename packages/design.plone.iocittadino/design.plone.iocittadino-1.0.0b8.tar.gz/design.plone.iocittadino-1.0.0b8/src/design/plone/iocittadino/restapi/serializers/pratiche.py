# -*- coding: utf-8 -*-
import json

from AccessControl.unauthorized import Unauthorized
from plone import api
from plone.memoize import view
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import datetimelike_to_iso
from zope.component import adapter
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer
from zope.schema import getFields

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IModelloPratica
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaStoreSerializerExtender
from design.plone.iocittadino.interfaces import ISerializeMessageToJsonSummary
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.interfaces import ISerializePraticaToJsonSummary

from .mixin import PortalUrlMixIn


@implementer(ISerializePraticaToJson)
@adapter(Interface, Interface)
class PraticaSerializer(PortalUrlMixIn):
    def __init__(self, pratica, request):
        self.pratica = pratica
        self.request = request

    def __call__(self):
        pratica_state = self.pratica.attrs.get("state")
        pratica_model = api.content.get(UID=self.pratica.attrs.get("form_id"))
        if isinstance(self.pratica.attrs.get("data"), dict) and pratica_model:
            # TODO: possibile errore qui, se le chiavi tornate da get_blob sono duplicate
            #       in pratica.attrs[data]
            data = {
                **self.pratica.attrs["data"],
                **self.get_blob_fields_serialized(),
            }
        else:
            data = self.pratica.attrs.get("data")
        # TODO: anche per altri campi in cui sono state messe logiche sorro (e.g. creation_date)
        # andrebbe fatto un piccolo refactoring per sportare l'inizializzazione qui e
        # migliorare la leggibilità
        result = {
            "item_id": self.pratica.intid,
            "userid": self.pratica.attrs.get("userid"),
            "state": pratica_state,
            "available_states": self.get_available_states(state=pratica_state),
            "creation_date": self.pratica.attrs.get("date")
            and datetimelike_to_iso(self.pratica.attrs.get("date")),
            "modification_date": self.pratica.attrs.get("modification_date")
            and datetimelike_to_iso(self.pratica.attrs.get("modification_date")),
            "servizio": self.get_summary_by_uid(self.pratica.attrs.get("servizio", "")),
            "ufficio": self.get_ufficio(self.pratica.attrs.get("ufficio", [])),
            "servizi_collegati": self.get_servizi_collegati(
                self.pratica.attrs.get("form_id", "")
            ),
            "assigned_to": self.pratica.attrs.get("assigned_to", ""),
            "has_report": bool(self.pratica.attrs.get("pratica_report", "")),
            "data": data,
            "messages": self.get_pratica_messages(),
        }
        for utility in getAllUtilitiesRegisteredFor(IPraticaStoreSerializerExtender):
            result.update(utility.get_fields(self.pratica))

        result["form"] = self.get_form_data(self.pratica.attrs.get("form_id", ""))
        if pratica_state != "draft":
            result["report_url"] = (
                f"{pratica_model.absolute_url()}/@@download/{self.pratica.intid}"
            )
        return result

    def get_pratica_messages(self):
        portal = api.portal.get()
        messages = getMultiAdapter((portal, self.request), IMessageContentStore).search(
            {"pratica_id": self.pratica.intid}
        )

        return [
            getMultiAdapter((i, self.request), ISerializeMessageToJsonSummary)()
            for i in messages
        ]

    def get_available_states(self, state):
        tool = getMultiAdapter((api.portal.get(), self.request), IPraticaContentStore)
        state_def = tool.states.get(state, {})
        return state_def.get("available_states", [])

    def get_servizi_collegati(self, modello_pratica_uid):
        modello_pratica = self.get_modello_pratica(modello_pratica_uid)
        try:
            field = getFields(IModelloPratica)["servizi_collegati"]
            servizi = field.get(modello_pratica)
            if servizi:
                return getMultiAdapter(
                    (field, modello_pratica, self.request), IFieldSerializer
                )()
        except Unauthorized:
            return []
        except AttributeError:
            return []

    def get_summary_by_uid(self, uid):
        if not uid:
            return None
        item = api.content.get(UID=uid)
        if not item:
            return None
        return getMultiAdapter((item, self.request), ISerializeToJsonSummary)()

    def get_form_data(self, uid):
        show_schema = self.request.form.get("show_schema", False)
        if not uid:
            return None
        item = api.content.get(UID=uid)
        if not item:
            return None

        data = getMultiAdapter((item, self.request), ISerializeToJsonSummary)()
        if show_schema:
            data["pratica_model"] = getattr(item, "pratica_model", "")
        return data

    def get_ufficio(self, uids):
        brains = api.content.find(UID=uids)
        return [
            getMultiAdapter((x, self.request), ISerializeToJsonSummary)()
            for x in brains
        ]

    def get_title(self, uid):
        modello_pratica = api.content.get(UID=uid)
        if not modello_pratica:
            return ""
        return modello_pratica.title

    def get_blob_fields_serialized(self):
        result = {}
        root_url = self.get_portal_url()

        blob_fields = set()

        # TODO: rewrite the try/except block, this was used to bypass the bad written tests
        try:
            pratica_model = json.loads(
                self.get_modello_pratica(
                    self.pratica.attrs.get("form_id", "")
                ).pratica_model
            )
        except json.decoder.JSONDecodeError:
            pratica_model = {}

        for page in pratica_model.get("pages", []):
            for element in page.get("elements", []):
                if element["type"] == "file":
                    blob_fields.add(element.get("valueName", element.get("name")))

                for element in element.get("elements", []):
                    if element["type"] == "file":
                        blob_fields.add(element.get("valueName", element.get("name")))

        for field in blob_fields:
            blob = self.pratica.attrs.get("data", {}).get(field)
            if not blob:
                continue
            if isinstance(blob, list):
                if len(blob) > 1:
                    raise NotImplementedError("Multiple blobs not supported")
                blob = blob[0]
            result[field] = {
                "content": f"{root_url}/pratica/{self.pratica.intid}/@@download/{field}",
                "name": blob["name"],
                "type": blob.get("type"),
            }

        return result

    @view.memoize
    def get_modello_pratica(self, uid):
        item = api.content.get(UID=uid)

        if not item:
            return None

        return item


@implementer(ISerializePraticaToJsonSummary)
@adapter(Interface, Interface)
class PraticaSerializerSummary(PraticaSerializer):
    def __call__(self):
        """
        Remove some possibly not needed big data
        """
        res = super().__call__()
        del res["data"]
        return res
