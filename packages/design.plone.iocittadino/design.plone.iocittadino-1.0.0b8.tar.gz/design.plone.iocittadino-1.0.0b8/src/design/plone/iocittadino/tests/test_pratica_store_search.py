# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperSearch(unittest.TestCase):
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
            email="doe@example.com",
            username="jdoe",
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
        self.modello_pratica2 = api.content.create(
            type="ModelloPratica",
            title="Example Modello 2",
            container=self.servizio,
        )
        self.modello_pratica3 = api.content.create(
            type="ModelloPratica",
            title="Example Modello 3",
            container=self.servizio,
        )
        self.modello_pratica4 = api.content.create(
            type="ModelloPratica",
            title="Example Modello 4",
            container=self.servizio,
        )
        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")
        api.content.transition(obj=self.modello_pratica2, transition="publish")
        api.content.transition(obj=self.modello_pratica3, transition="publish")
        api.content.transition(obj=self.modello_pratica4, transition="publish")

        # create some records
        login(self.portal, "foo")
        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        )
        self.tool.add(
            {
                "form_id": self.modello_pratica2.UID(),
                "data": "another value from foo",
            }
        )
        self.tool.add(
            {
                "form_id": self.modello_pratica3.UID(),
                "data": "third foo value",
            }
        )
        id = self.tool.add(
            {
                "form_id": self.modello_pratica4.UID(),
                "data": "foo value completed",
            }
        ).intid

        login(self.portal, "jdoe")
        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "jdoe value",
            }
        )

        # change state
        login(self.portal, TEST_USER_NAME)
        self.tool.update_state(item_id=id, state="completed")

    def tearDown(self):
        self.tool.clear()

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_without_params_admin_see_all_records(self):
        res = self.tool.search()
        self.assertEqual(len(res), 5)

    def test_without_params_user_see_only_his_records(self):
        login(self.portal, "foo")
        res = self.tool.search()
        self.assertEqual(len(res), 4)

        login(self.portal, "jdoe")
        res = self.tool.search()
        self.assertEqual(len(res), 1)

    def test_search_by_state(self):
        res = self.tool.search(query={"state": "draft"})
        self.assertEqual(len(res), 1)

        res = self.tool.search(query={"state": "ongoing"})
        self.assertEqual(len(res), 3)

        res = self.tool.search(query={"state": "completed"})
        self.assertEqual(len(res), 1)

        res = self.tool.search(query={"state": ["ongoing", "draft"]})
        self.assertEqual(len(res), 4)

    def test_search_by_user(self):
        res = self.tool.search(query={"userid": "foo"})
        self.assertEqual(len(res), 4)

        res = self.tool.search(query={"userid": "jdoe"})
        self.assertEqual(len(res), 1)
