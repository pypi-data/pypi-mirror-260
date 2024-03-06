# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zExceptions import NotFound
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperDelete(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def tearDown(self):
        self.pratica_storage.clear()
        self.message_storage.clear()

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_delete_record_return_error_if_id_not_found(self):
        self.assertRaises(NotFound, self.message_storage.delete, item_id=1222)

    def test_delete_raise_valuerror_if_no_pratica_id_passed(self):
        self.assertRaises(NotFound, self.message_storage.delete, item_id=122)

    def test_delete_record(self):
        servizio = api.content.create(
            type="Servizio",
            id="example-service",
            title="Example Service",
            container=self.portal,
        )

        modello_pratica = api.content.create(
            type="ModelloPratica",
            id="example-modello",
            title="Example Modello",
            container=servizio,
        )

        pratica_id = self.pratica_storage.add(
            {
                "form_id": modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        message = self.message_storage.add(
            {"pratica_id": pratica_id, "message": "message"}
        )

        self.assertEqual(self.message_storage.length, 2)

        self.message_storage.delete(item_id=message.intid)

        self.assertEqual(self.message_storage.length, 1)
