# -*- coding: utf-8 -*-
import datetime
import unittest

import freezegun
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zExceptions import NotFound
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperTransition(unittest.TestCase):
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
        self.tool.clear()

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_update_state_raise_error_if_missing_parameters(self):
        self.assertRaises(
            TypeError,
            self.tool.update_state,
        )

        self.assertRaises(
            TypeError,
            self.tool.update_state,
            item_id=111,
        )

        # error because wrong data
        self.assertRaises(
            NotFound,
            self.tool.update_state,
            item_id=111,
            state="foo",
        )

    def test_update_state_raise_error_if_wrong_pratica_id(self):
        self.assertRaises(
            NotFound,
            self.tool.update_state,
            item_id=1222,
            state="foo",
        )

    def test_update_state_return_error_if_state_is_wrong(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        with self.assertRaises(ValueError) as cm:
            self.tool.update_state(item_id=id, state="foo")

        self.assertEqual("Unknown state: foo.", str(cm.exception))

    def test_update_state_return_error_if_next_state_isnt_correct(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        item = self.tool.get(id)

        self.assertEqual(item.attrs.get("state"), "ongoing")

        # with self.assertRaises(ValueError) as cm:
        #     self.tool.update_state(item_id=id, state="draft")
        #     self.assertEqual(
        #         "Unable to change state from ongoing to draft.", str(cm.exception)
        #     )

    def test_update_state_success(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        item = self.tool.get(id)

        self.assertEqual(item.attrs.get("state"), "ongoing")
        self.tool.update_state(item_id=id, state="completed")

        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "completed")

    def test_from_draft_can_only_go_to_ongoing(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid
        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="draft")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="completed")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="suspended")

        self.tool.update_state(item_id=id, state="ongoing")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "ongoing")

    def test_from_ongoing_can_go_on_suspended(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        self.tool.update_state(item_id=id, state="suspended")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "suspended")

    def test_from_ongoing_can_go_on_completed(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        self.tool.update_state(item_id=id, state="completed")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "completed")

    def test_from_ongoing_can_go_on_canceled(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        # or on canceled
        self.tool.update_state(item_id=id, state="canceled")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "canceled")

    def test_from_suspended_can_go_back_on_ongoing(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        self.tool.update_state(item_id=id, state="suspended")

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        self.tool.update_state(item_id=id, state="ongoing")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "ongoing")

    def test_from_suspended_can_go_back_on_completed(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        self.tool.update_state(item_id=id, state="suspended")

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        # or go back on completed
        self.tool.update_state(item_id=id, state="completed")
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("state"), "completed")

    def test_from_completed_cant_go_anywhere(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        self.tool.update_state(item_id=id, state="completed")

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="ongoing")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="suspended")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="canceled")

    def test_from_canceled_cant_go_anywhere(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        self.tool.update_state(item_id=id, state="canceled")

        # with self.assertRaises(ValueError):
        #     self.tool.update_state(item_id=id, state="draft")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="ongoing")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="suspended")

        with self.assertRaises(ValueError):
            self.tool.update_state(item_id=id, state="completed")

    def test_ongoing_date_is_being_set_automatically_when_update_state(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        testing_time = datetime.datetime.utcnow()

        with freezegun.freeze_time(testing_time):
            self.tool.update_state(item_id=id, state="ongoing")

        self.assertEquals(self.tool.get(id).attrs.get("ongoing_date"), testing_time)
