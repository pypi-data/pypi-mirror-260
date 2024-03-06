# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from zope.component import getMultiAdapter
from zope.component import getSiteManager

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestAssignTo(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.servizio = api.content.create(
            type="Servizio",
            id="example-service",
            title="Example Service",
            container=self.portal,
        )

        self.modello_pratica = api.content.create(
            type="ModelloPratica",
            id="example-modello",
            title="Example Modello",
            container=self.servizio,
        )

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )

        self.portal.MailHost = mailhost = MockMailHost("MailHost")
        api.portal.set_registry_record("plone.email_from_address", "noreply@foo.com")
        sm = getSiteManager(context=self.portal)

        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def tearDown(self):
        self.pratica_store.clear()

    @property
    def pratica_store(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_notify_when_set_assign_to(self):
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 0)

        pratica_id = self.pratica_store.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "assigned_to": "foo",
            }
        ).intid

        self.assertEqual(len(mailhost.messages), 1)
        self.assertIn(
            f"Subject: Pratica assegnata: {pratica_id}",
            mailhost.messages[0].decode(),
        )
