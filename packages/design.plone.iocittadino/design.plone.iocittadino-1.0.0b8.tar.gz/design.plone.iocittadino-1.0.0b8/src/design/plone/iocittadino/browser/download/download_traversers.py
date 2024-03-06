# -*- coding: utf-8 -*-
import json

from plone import api
from plone.memoize import view
from plone.namedfile import NamedBlobFile
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino.interfaces import IBlobTraverse
from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IMessageTraverse
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaTraverse

# from design.plone.iocittadino.interfaces import IBlobStorage


@implementer(IPraticaTraverse)
class PraticaTraverser(BrowserView):
    pratica_id = None

    def publishTraverse(self, request, name):
        if self.pratica_id is None:
            self.pratica_id = name
        return self

    @view.memoize
    def get_praticastore(self):
        return queryMultiAdapter((api.portal.get(), self.request), IPraticaContentStore)

    def get_pratica(self):
        return self.get_praticastore().get(item_id=self.pratica_id)


@implementer(IMessageTraverse)
class MessageTraverser(BrowserView):
    message_id = None

    def publishTraverse(self, request, name):
        if self.message_id is None:
            self.message_id = name
        return self

    def get_message(self):
        if self.message_id is None:
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
            return tool.get(item_id=self.message_id)
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


@implementer(IBlobTraverse)
class BlobTraverser(BrowserView):
    """Blob upload files view also taverser intermediate view for @@dowload"""

    file_id = None

    def publishTraverse(self, request, name):
        self.name = name

        return self

    def __call__(self, *args, **kwargs):
        if self.request["REQUEST_METHOD"] == "POST":
            self.request.response.setHeader("Content-Type", "application/json")
            return json.dumps(self.save_files())

        return None

    def save_files(self):
        """Save file to blob storage"""
        alsoProvides(self.request, IDisableCSRFProtection)
        # blob_storage = getMultiAdapter(
        #     (api.portal.get(), self.request), IBlobStorage
        # ).get_storage()
        pratica_store = queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        )

        response = {}

        for key, file in self.request.form.items():
            content_type = [
                header[1]
                for header in file.headers.items()
                if header[0] == "Content-Type"
            ][0]

            # response[key] = blob_storage.add(
            #     NamedBlobFile(
            #         data=file.read(),
            #         contentType=content_type,
            #         filename=file.filename,
            #     )
            # )

            response[key] = pratica_store.store.add_tempfile(
                NamedBlobFile(
                    data=file.read(),
                    contentType=content_type,
                    filename=file.filename,
                )
            )
            file.close()

        return response
