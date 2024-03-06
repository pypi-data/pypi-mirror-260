# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zExceptions import NotFound
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperPatch(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.tool = getMultiAdapter((self.portal, self.request), IPraticaContentStore)
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

    def test_update_record_return_error_if_id_not_passed(self):
        self.assertRaises(
            TypeError,
            self.tool.update,
        )

    def test_update_record_return_error_if_id_not_found(self):
        self.assertRaises(
            NotFound,
            self.tool.update,
            item_id=1222,
            data=dict(data="foo"),
        )

    def test_update_record_return_error_if_state_is_wrong(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        self.assertRaises(
            ValueError,
            self.tool.update,
            item_id=id,
            data=dict(state="foo", data="foo"),
        )

    def test_update_record(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("userid", None), api.user.get_current().getId())
        self.assertEqual(item.attrs.get("data", None), "some value")

        self.tool.update(item_id=id, data=dict(data="xxx"))

        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("userid", None), api.user.get_current().getId())
        self.assertEqual(item.attrs.get("data", None), "xxx")

    def test_update_record_skip_unknown_fields(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        self.tool.update(item_id=id, data=dict(data="xxx", unknown="foo"))

        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("userid", None), api.user.get_current().getId())
        self.assertEqual(item.attrs.get("data", None), "xxx")
        self.assertNotIn("unknown", item.attrs.keys())

    def test_cant_update_if_state_not_draft(self):
        # default initial state is ongoing
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        with self.assertRaises(ValueError) as cm:
            self.tool.update(item_id=id, data=dict(data="xxx", unknown="foo"))

        self.assertEqual(
            "Unable to edit a Pratica not in draft state.", str(cm.exception)
        )

    def test_cant_update_if_state_is_draft_but_data_not_passed(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        with self.assertRaises(ValueError) as cm:
            self.tool.update(item_id=id, data=dict(foo="xxx", unknown="foo"))

        self.assertEqual(
            "Missing required field: data or assigned_to.", str(cm.exception)
        )

    def test_can_update_assign_in_draft_state(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "draft",
            }
        ).intid

        self.tool.update(item_id=id, data=dict(assigned_to="jdoe"))
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("assigned_to", None), "jdoe")

    def test_can_update_assign_in_ongoing_state(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid

        self.tool.update(item_id=id, data=dict(assigned_to="jdoe"))
        item = self.tool.get(id)
        self.assertEqual(item.attrs.get("assigned_to", None), "jdoe")

    def test_cant_update_assign_in_suspended_state(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        self.tool.update_state(item_id=id, state="suspended")

        with self.assertRaises(ValueError) as cm:
            self.tool.update(item_id=id, data=dict(assigned_to="jdoe"))

        self.assertEqual(
            "Unable to assign a Pratica to an user when is in a final state.",
            str(cm.exception),
        )

    def test_cant_update_assign_in_completed_state(self):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
            }
        ).intid
        self.tool.update_state(item_id=id, state="completed")

        with self.assertRaises(ValueError) as cm:
            self.tool.update(item_id=id, data=dict(assigned_to="jdoe"))

        self.assertEqual(
            "Unable to assign a Pratica to an user when is in a final state.",
            str(cm.exception),
        )
