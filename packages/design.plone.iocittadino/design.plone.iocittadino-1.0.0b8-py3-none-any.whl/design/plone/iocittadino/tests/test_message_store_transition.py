# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperMessageTransition(unittest.TestCase):
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
        self.pratica_id = self.pratica_storage.add(
            {"form_id": self.modello_pratica.UID(), "data": "some data"}
        ).intid

        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")

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

    def tearDown(self):
        self.pratica_storage.clear()
        self.message_storage.clear()

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    def test_update_state_raise_error_if_missing_parameters(self):
        self.assertRaises(
            TypeError,
            self.message_storage.update_state,
        )

        self.assertRaises(
            TypeError,
            self.message_storage.update_state,
            item_id=111,
        )

        # error because wrong data
        self.assertRaises(
            NotFound,
            self.message_storage.update_state,
            item_id=111,
            state="foo",
        )

    # TODO: Make structured control of all the shit below in one generic method
    def test_update_state_raise_error_if_wrong_pratica_id(self):
        self.assertRaises(
            NotFound,
            self.message_storage.update_state,
            item_id=1222,
            state="foo",
        )

    def test_update_state_return_error_if_state_is_wrong(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some message",
            }
        ).intid

        with self.assertRaises(ValueError) as cm:
            self.message_storage.update_state(item_id=id, state="foo")

        self.assertEqual("Unknown state: foo.", str(cm.exception))

    def test_update_state_return_error_if_next_state_isnt_correct(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
            }
        ).intid

        item = self.message_storage.get(id)

        self.assertEqual(item.attrs.get("state"), "pending")
        with self.assertRaises(ValueError) as cm:
            self.message_storage.update_state(item_id=id, state="seen")

        self.assertEqual(
            "Unable to change state from pending to seen.", str(cm.exception)
        )

    def test_update_state_success(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some message",
            }
        ).intid

        item = self.message_storage.get(id)

        self.assertEqual(item.attrs.get("state"), "pending")
        self.message_storage.update_state(item_id=id, state="sent")

        item = self.message_storage.get(id)
        self.assertEqual(item.attrs.get("state"), "sent")

    def test_from_pending_can_only_go_to_sent(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
            }
        ).intid
        with self.assertRaises(ValueError):
            self.message_storage.update_state(item_id=id, state="seen")

        self.message_storage.update_state(item_id=id, state="sent")
        item = self.message_storage.get(id)
        self.assertEqual(item.attrs.get("state"), "sent")

    def test_from_sent_can_only_go_to_seen(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
            }
        ).intid
        with self.assertRaises(ValueError):
            self.message_storage.update_state(item_id=id, state="seen")

        self.message_storage.update_state(item_id=id, state="sent")

        self.message_storage.update_state(item_id=id, state="seen")

        item = self.message_storage.get(id)
        self.assertEqual(item.attrs.get("state"), "seen")

    def test_from_seen_cant_go_anywhere(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
            }
        ).intid
        self.message_storage.update_state(item_id=id, state="sent")
        self.message_storage.update_state(item_id=id, state="seen")

        with self.assertRaises(ValueError):
            self.message_storage.update_state(item_id=id, state="sent")

        with self.assertRaises(ValueError):
            self.message_storage.update_state(item_id=id, state="pending")

    @unittest.skip("Da errori con il servizio")
    def test_normal_user_can_only_seen_transition(self):
        login(self.portal, "foo")
        pratica_id = self.pratica_storage.add(
            {"form_id": self.modello_pratica.UID(), "data": "some data"}
        ).intid

        logout()
        login(self.portal, "gestore")
        id = self.message_storage.add(
            {
                "pratica_id": pratica_id,
                "message": "some value",
            }
        ).intid

        logout()
        login(self.portal, "foo")

        with self.assertRaises(Unauthorized):
            self.message_storage.update_state(item_id=id, state="sent")

        logout()
        login(self.portal, "gestore")

        self.message_storage.update_state(item_id=id, state="sent")

        logout()
        login(self.portal, "foo")

        self.message_storage.update_state(item_id=id, state="seen")
