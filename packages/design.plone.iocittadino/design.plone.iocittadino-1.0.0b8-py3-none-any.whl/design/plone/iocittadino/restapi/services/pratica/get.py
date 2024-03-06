# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from plone import api
from plone.memoize import view
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaTraverse
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.interfaces import ISerializePraticaToJsonSummary
from design.plone.iocittadino.interfaces import IUserStore


@implementer(IPraticaTraverse)
class GetRecord(Service):
    """
    Get single record
    """

    item_id = None

    def publishTraverse(self, request, name):
        if self.item_id is None:
            self.item_id = name
        return self

    def reply(self):
        """ """
        praticastore = self.get_praticastore()

        if self.item_id is None:
            # new pratica / defaultValues
            # TODO: definire una api  in praticastore per ottenere le pratiche in corso di un utente per un modellopratica e
            #       usare quella qui e nel validatore di add.py
            if self.request.form.get("form_id"):
                pratiche = praticastore.search(
                    query={
                        "userid": api.user.get_current().getId(),
                        # self.context.UID(), il contesto attualmente è la root del sito
                        "form_id": self.request.form["form_id"],
                        # TODO: la semantica di "allowed_states" per la pratica non è chiara,
                        #       forse è meglio usare "in_progress_states"?
                        "state": praticastore.allowed_states,
                    }
                )
            else:
                pratiche = []
            if pratiche:
                # XXX: due opzioni:
                #      a - si risponde con questo errore se c'è già una pratica in corso
                #      b - si risponde con la pratica in corso
                # raise ValueError(
                #     translate(
                #         _(
                #             "duplicate_pratica",
                #             default="Unable to submit a new Record. There is already a Record in progress for this Service.",
                #         ),
                #         context=self.request,
                #     )
                # )
                return queryMultiAdapter(
                    (pratiche[0], self.request), ISerializePraticaToJson
                )()
            else:
                user = api.user.get_current()
                userstore = queryMultiAdapter(
                    (self.context, user, self.request), IUserStore
                )
                defaults = userstore.get()
                return {
                    "data": defaults,
                }
        else:
            try:
                record = self.get_pratica()
            except ValueError:
                raise BadRequest(
                    translate(
                        _(
                            "bad_pratica_id",
                            default="Bad parameter value was passed",
                        ),
                        context=self.request,
                    )
                )

            return queryMultiAdapter((record, self.request), ISerializePraticaToJson)()

    @view.memoize
    def get_praticastore(self):
        return queryMultiAdapter((api.portal.get(), self.request), IPraticaContentStore)

    def get_pratica(self):
        return self.get_praticastore().get(item_id=self.item_id)


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class RecordsData(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"data": {"@id": "{}/@pratiche".format(self.context.absolute_url())}}
        if not expand:
            return result

        store = queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        )
        query = unflatten_dotted_dict(self.request.form)
        if query:
            records = store.search(query=query)
        else:
            records = store.search()
        items = []
        services = []
        for record in records:
            try:
                if "fullobjects" in list(query):
                    data = queryMultiAdapter(
                        (record, self.request),
                        ISerializePraticaToJson,
                    )()

                else:
                    data = queryMultiAdapter(
                        (record, self.request),
                        ISerializePraticaToJsonSummary,
                    )()
                items.append(data)

                found_service = False
                for service in services:
                    if service["@id"] == data["servizio"]["@id"]:
                        found_service = True
                        break
                if not found_service:
                    services.append(data["servizio"])
            except Unauthorized:
                # skip: user can't access some pratica related infos
                continue

        data = {
            "@id": "{}/@pratiche".format(self.context.absolute_url()),
            "items": items,
            "items_total": len(items),
            "services": services,
        }

        result["data"] = data
        return result


class GetRecordList(Service):
    """GET /@pratiche"""

    def reply(self):
        data = RecordsData(self.context, self.request)
        return data(expand=True).get("data", {})
