# -*- coding: utf-8 -*-
import base64
from urllib.request import urlopen

from plone import api

# from design.plone.iocittadino.interfaces import IBlobStorage
from plone.namedfile.utils import get_contenttype
from plone.namedfile.utils import stream_data
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.component import queryMultiAdapter

from design.plone.iocittadino import _
from design.plone.iocittadino.interfaces import IPraticaContentStore


class ModelloPraticaReportDownload(BrowserView):
    """View to download the pratica report by id"""

    def __init__(self, context, request):
        super().__init__(context, request)
        self.pratica_id = None

    def publishTraverse(self, request, name):
        if self.pratica_id is None:
            self.pratica_id = name
        else:
            raise NotFound(self, name, request)
        return self

    def __call__(self):
        """View to download the pratica report by id"""
        pratica = self.pratica_id and queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        ).get(self.pratica_id)
        pratica_report = pratica.attrs.get("pratica_report", {})
        if not pratica_report:
            raise NotFound(_("The pdf record was not found"))

        # handle case we have an old pratica saved as base64 encoded stream
        if type(pratica_report) is dict:
            blob = pratica_report.get("blob")

        if blob:
            self.request.response.setHeader(
                "Content-Length", pratica_report.get("blob").getSize()
            )
            self.request.response.setHeader("Content-Type", "application/pdf")
            self.request.response.setHeader(
                "Content-Disposition",
                'attachment; filename="{filename}"'.format(
                    filename=pratica_report.get("name")
                ),
            )
            # TODO: Last modified deve essere lat modified, non now
            # self.request.response.setHeader("Last-Modified", DateTime.rfc822(DateTime()))
            return stream_data(blob)

        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader(
            "Content-Disposition",
            f'attachment; filename="{self.context.getId()}.pdf"',
        )
        # TODO: Last modified deve essere lat modified, non now
        # self.request.response.setHeader("Last-Modified", DateTime.rfc822(DateTime()))
        return self.get_content(pratica)

    def get_content(self, pratica):
        """The method gets and decodes the base64 encoded file from a pratica"""
        pdf_record = pratica.attrs.get("pratica_report", None)
        if not pdf_record:
            raise NotFound(_("The pdf record was not found"))
        return base64.b64decode(pratica.attrs.get("pratica_report", None))


# TODO: la vista ha il permesso di view, verificare che però non sia accessibile
#       da utenti che non hanno il permesso di view sul messaggio
class MessageAttachmentDownload(BrowserView):
    """Download message attachments file, used in the traversing chain under the
    @message view

    * the context is the RestAPi GET "@message/<intid>" view

    /message/<intid>/@@download/<fileindex>/<filename>
                                 ^^^^^^^^^^^^^^^^^^^^^^
    """

    fileindex = None
    filename = None

    def publishTraverse(self, request, name):
        if self.fileindex is None:
            self.fileindex = int(name)
        elif self.filename is None:
            self.filename = name
        return self

    def __call__(self):
        message = self.context.get_message()
        try:
            attachment = message.attrs.get("attachments", [])[self.fileindex]
        except IndexError:
            raise NotFound("No attachment found")
        response = self.request.response

        response.setHeader(
            "Content-Disposition",
            f'attachment; filename="{attachment.get("name") or "attachment"}"',
        )
        # TODO: Last modified deve essere lat modified, non now
        # self.request.response.setHeader("Last-Modified", DateTime.rfc822(DateTime()))
        blob = attachment.get("blob")
        if blob:
            contenttype = get_contenttype(blob)
            response.setHeader("Content-Type", contenttype)
            response.setHeader("Content-Length", blob.getSize())
            return stream_data(blob)
        # OBSOLETED
        data = attachment.get("data")
        if data and data.startswith("data:"):
            # TODO: headers
            return urlopen(data).getvalue()
        raise NotFound("No data")


class PraticaBlobFieldDownload(BrowserView):
    """Download pratica blob field file, used in the traversing chain over the
    pratica view

    /pratica/<intid>/@@download/<fieldname>
                                ^^^^^^^^^^^^
    """

    fieldname = None

    def publishTraverse(self, request, name):
        if self.fieldname is None:
            self.fieldname = name
        return self

    def __call__(self):
        pratica = self.context.get_pratica()
        blob = pratica.attrs.get("data", {}).get(self.fieldname)

        if not blob:
            raise NotFound("No attachment found")
        if isinstance(blob, list):
            if len(blob) > 1:
                raise NotImplementedError("Multiple blobs not supported")
            blob = blob[0]

        response = self.request.response
        # response.setHeader(
        #     "Content-Disposition",
        #     f'attachment; filename="{blob.get("name") or "attachment"}"',
        # )
        # TODO: Last modified deve essere lat modified, non now
        # self.request.response.setHeader("Last-Modified", DateTime.rfc822(DateTime()))
        blob = blob.get("blob")
        if blob:
            contenttype = get_contenttype(blob)
            response.setHeader("Content-Type", contenttype)
            response.setHeader("Content-Length", blob.getSize())
            return stream_data(blob)
        else:
            raise NotFound("No data")


class BlobDownload(BrowserView):
    """View to download a temporary blob report by id"""

    file_id = None

    def publishTraverse(self, request, file_id):
        self.file_id = file_id

        return self

    def __call__(self):
        """View to download the blob by id"""
        file_id = self.file_id or ""
        pratica_store = queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        )
        # blob = (
        #     getMultiAdapter((api.portal.get(), self.request), IBlobStorage)
        #     .get_storage()
        #     .get(file_id, {})
        # )

        blob = pratica_store.store.get_tempfile(file_id)

        if not blob:
            raise NotFound(_("The blob was not found"))

        if blob:
            self.request.response.setHeader("Content-Length", blob.getSize())
            self.request.response.setHeader("Content-Type", blob.contentType)
            self.request.response.setHeader(
                "Content-Disposition",
                'attachment; filename="{filename}"'.format(filename=blob.filename),
            )
            return stream_data(blob)
