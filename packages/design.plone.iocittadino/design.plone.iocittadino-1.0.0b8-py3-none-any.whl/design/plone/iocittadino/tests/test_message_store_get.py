# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from zExceptions import Unauthorized
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperMessageGet(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )
        api.user.create(
            email="gestore@example.com",
            username="gestore",
            password="secret123",
        )

        setRoles(self.portal, "gestore", ["Gestore Pratiche"])

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

        self.pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        self.message_id = self.message_storage.add(
            {"pratica_id": self.pratica_id, "message": self.message_text}
        ).intid

        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")

    def tearDown(self):
        self.pratica_storage.clear()
        self.message_storage.clear()

    @property
    def message_text(self):
        """The message text for testing"""
        return "Testing message"

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    def test_get_raise_not_found_if_missing_message_id(self):
        self.assertRaises(TypeError, self.message_storage.get)

    def test_get_return_none_if_wrong_type(self):
        self.assertRaises(ValueError, self.message_storage.get, item_id="foo")

    # TODO: Usare il mock
    @unittest.skip("Da errori con il servizio")
    def test_anon_can_not_get_record(self):
        logout()
        self.assertRaises(
            Unauthorized, self.message_storage.get, item_id=self.message_id
        )

    @unittest.skip("Da errori con il servizio")
    def test_normal_user_can_not_get_record_from_other_users(self):
        login(self.portal, "foo")
        self.assertRaises(
            Unauthorized, self.message_storage.get, item_id=self.message_id
        )

    def test_admin_can_get_record(self):
        record = self.message_storage.get(item_id=self.message_id)
        self.assertEqual(record.attrs.get("message"), self.message_text)

    @unittest.skip("Da errori con il servizio")
    def test_normal_user_can_get_its_record(self):
        login(self.portal, "foo")
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        logout()
        login(self.portal, "gestore")
        message_id = self.message_storage.add(
            {"pratica_id": pratica_id, "message": self.message_text}
        )

        record = self.message_storage.get(item_id=message_id)

        self.assertEqual(record.attrs.get("message"), self.message_text)
