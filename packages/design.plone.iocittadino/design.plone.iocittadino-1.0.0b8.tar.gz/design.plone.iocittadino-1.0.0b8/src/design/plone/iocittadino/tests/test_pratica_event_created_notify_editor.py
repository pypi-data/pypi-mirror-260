# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestNotifyEditorAboutPraticaCreation(unittest.TestCase):
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

    def tearDown(self):
        self.pratica_store.clear()
        self.message_store.clear()

    @property
    def pratica_store(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_store(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    def test_notify_success(self):
        record = self.pratica_store.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "email": "email@email.com",
            }
        )

        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_store.length, 1)
        self.pratica_store.update_state(item_id=record.intid, state="completed")
        self.assertEqual(self.message_store.length, 2)
