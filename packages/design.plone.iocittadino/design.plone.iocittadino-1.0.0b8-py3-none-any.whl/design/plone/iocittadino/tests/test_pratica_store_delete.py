# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zExceptions import NotFound
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperDelete(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.tool = getMultiAdapter((self.portal, self.request), IPraticaContentStore)

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
        self.tool.clear()

    def test_delete_record_return_error_if_id_not_found(self):
        self.assertRaises(NotFound, self.tool.delete, item_id=1222)

    def test_delete_raise_valuerror_if_no_pratica_id_passed(self):
        self.assertRaises(ValueError, self.tool.delete, item_id="")

    def test_can_delete_record_in_draft_state(self):
        record_id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        self.assertEqual(self.tool.length, 1)

        self.tool.delete(item_id=record_id)

        self.assertEqual(self.tool.length, 0)

    def test_cant_delete_record_in_ongoing_state(self):
        data = {
            "form_id": self.modello_pratica.UID(),
            "data": "some value",
        }
        record_id = self.tool.add(data).intid

        # initial state is ongoing
        with self.assertRaises(ValueError) as cm:
            self.tool.delete(item_id=record_id)

        self.assertEqual(
            "You can't delete a record in this state: ongoing",
            str(cm.exception),
        )

    def test_cant_delete_record_in_suspended_state(self):
        data = {
            "form_id": self.modello_pratica.UID(),
            "data": "some value",
        }
        record_id = self.tool.add(data).intid

        self.tool.update_state(item_id=record_id, state="suspended")
        with self.assertRaises(ValueError) as cm:
            self.tool.delete(item_id=record_id)

        self.assertEqual(
            "You can't delete a record in this state: suspended",
            str(cm.exception),
        )

    def test_cant_delete_record_in_completed_state(self):
        data = {
            "form_id": self.modello_pratica.UID(),
            "data": "some value",
        }
        record_id = self.tool.add(data).intid

        self.tool.update_state(item_id=record_id, state="completed")
        with self.assertRaises(ValueError) as cm:
            self.tool.delete(item_id=record_id)

        self.assertEqual(
            "You can't delete a record in this state: completed",
            str(cm.exception),
        )
