# -*- coding: utf-8 -*-
from plone import api
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
from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IMessageTraverse
from design.plone.iocittadino.interfaces import ISerializeMessageToJson


@implementer(IMessageTraverse)
class GetRecord(Service):
    """
    Get single record

    """

    record_id = None

    def publishTraverse(self, request, name):
        if self.record_id is None:
            self.record_id = name
        return self

    def get_message(self):
        if self.record_id is None:
            raise BadRequest(
                translate(
                    _(
                        "missing_pratica_id_label",
                        default="Required record is missing.",
                    ),
                    context=self.request,
                )
            )

        portal = api.portal.getSite()
        tool = queryMultiAdapter((portal, self.request), IMessageContentStore)

        try:
            return tool.get(item_id=self.record_id)
        except ValueError:
            raise BadRequest(
                translate(
                    _(
                        "bad_value_passed",
                        default="Passed id is not valid.",
                    ),
                    context=self.request,
                )
            )

    def reply(self):
        """ """
        return queryMultiAdapter(
            (self.get_message(), self.request), ISerializeMessageToJson
        )()


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class RecordsData(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"data": {"@id": "{}/@messages".format(self.context.absolute_url())}}
        if not expand:
            return result

        portal = api.portal.getSite()
        store = queryMultiAdapter((portal, self.request), IMessageContentStore)

        query = unflatten_dotted_dict(self.request.form)
        # TODO: per l'utente senza privilegi, filtrare i messaggi per userid
        #       (viene fatto dentro la search?)
        if query:
            data = store.search(query=query)
        else:
            data = store.search()

        items = [
            queryMultiAdapter((x, self.request), ISerializeMessageToJson)()
            for x in data
        ]
        data = {
            "@id": "{}/@messages".format(self.context.absolute_url()),
            "items": items,
            "items_total": len(items),
        }

        result["data"] = data
        return result


class GetRecordList(Service):
    def reply(self):
        data = RecordsData(self.context, self.request)
        return data(expand=True).get("data", {})
