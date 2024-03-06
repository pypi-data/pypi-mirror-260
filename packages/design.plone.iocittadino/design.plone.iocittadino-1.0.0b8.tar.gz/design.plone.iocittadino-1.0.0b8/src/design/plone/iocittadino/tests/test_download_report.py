# -*- coding: utf-8 -*-
import unittest
from base64 import b64encode

from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.zope import Browser
from transaction import commit
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaPdfGenerator

from ..testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestDownload(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer["app"])
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.servizio = api.content.create(
            type="Servizio",
            id="example-service",
            title="Example Service",
            container=self.portal,
        )
        api.content.transition(obj=self.servizio, transition="publish")
        self.modello_pratica = api.content.create(
            type="ModelloPratica",
            id="example-modello",
            title="Example Modello",
            container=self.servizio,
            pratica_model="foo schema",
        )
        api.content.transition(obj=self.modello_pratica, transition="publish")
        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )

        self.pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "pratica_report": b64encode(b"encoded to base64 file"),
            }
        ).intid
        commit()

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_download_own_report(self):
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )
        self.browser.open(
            f"{self.modello_pratica.absolute_url()}/@@download/{self.pratica_id}",
        )
        self.assertEqual(self.browser._response.status, "200 OK")
        self.assertTrue(self.browser.contents)

    def test_anonymous_cant_download_report(self):
        # self.browser.followRedirects = False
        self.browser.open(
            f"{self.modello_pratica.absolute_url()}/@@download/{self.pratica_id}",
        )
        # TODO: follows redirect to login page
        self.assertTrue(
            self.browser.url.startswith("http://nohost/plone/login?came_from=")
        )

    def test_cant_download_not_own_report(self):
        # self.browser.followRedirects = False
        self.browser.addHeader(
            "Authorization",
            "Basic foo:secret123",
        )
        self.browser.open(
            f"{self.modello_pratica.absolute_url()}/@@download/{self.pratica_id}",
        )
        # self.assertEqual(self.browser._response.status, "401 Unauthorized")
        # TODO: follows redirect to insufficient privileges page
        self.assertEqual(
            self.browser.url, "http://nohost/plone/insufficient-privileges"
        )

    def test_generate_pdf(self):
        pdf_generator = queryMultiAdapter(
            (self.modello_pratica, self.request), IPraticaPdfGenerator
        )
        pratica = self.pratica_storage.get(self.pratica_id)
        self.assertEqual(pdf_generator.write_pdf(pratica)[:4], b"%PDF")
