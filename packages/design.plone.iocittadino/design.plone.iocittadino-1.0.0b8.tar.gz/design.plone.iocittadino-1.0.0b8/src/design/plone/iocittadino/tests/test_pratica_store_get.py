# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from zExceptions import Unauthorized
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperGet(unittest.TestCase):
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

        self.pratica_id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")

    def tearDown(self):
        self.tool.clear()

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_get_raise_type_error_if_missing_pratica_id(self):
        self.assertRaises(TypeError, self.tool.get)

    def test_get_raise_not_found_if_wrong_type(self):
        self.assertRaises(ValueError, self.tool.get, item_id="foo")

    @unittest.skip("Da errori con il CT servizio")
    def test_anon_can_not_get_record(self):
        logout()
        self.assertRaises(Unauthorized, self.tool.get, item_id=self.pratica_id)

    @unittest.skip("Da errori con il servizio")
    def disabled_test_normal_user_can_not_get_pratica_record_from_other_users(
        self,
    ):
        login(self.portal, "foo")
        self.assertRaises(Unauthorized, self.tool.get, item_id=self.pratica_id)

    def test_admin_can_get_record(self):
        record = self.tool.get(item_id=self.pratica_id)
        self.assertEqual(record.attrs.get("data"), "some value")

    @unittest.skip("Da errori con il CT servizio")
    def disabled_test_normal_user_can_get_its_record(self):
        login(self.portal, "foo")
        pratica_id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "another value",
            }
        )
        record = self.tool.get(item_id=pratica_id)
        self.assertEqual(record.attrs.get("data"), "another value")
