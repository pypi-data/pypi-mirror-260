# -*- coding: utf-8 -*-
import json
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from transaction import commit
from zExceptions.unauthorized import Unauthorized
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IUserStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestUserStore(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal._original_MailHost = self.portal.MailHost
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )
        api.user.create(
            email="jdoe@example.com",
            username="jdoe",
            password="secret123",
        )

        commit()

    def get_tool(self, user):
        return getMultiAdapter((self.portal, user, self.request), IUserStore)

    def test_set_return_error_if_user_try_to_set_from_other_user(self):
        with api.env.adopt_user(username="foo"):
            tool = self.get_tool(user=api.user.get(username="jdoe"))
            with self.assertRaises(Unauthorized) as cm:
                tool.set(data={})
            self.assertEqual(
                "You can't update user properties for a different user.",
                str(cm.exception),
            )

    def test_set_ok_if_same_user(self):
        with api.env.adopt_user(username="foo"):
            tool = self.get_tool(user=api.user.get(username="foo"))
            data = tool.get()
            self.assertEqual(data["email"], "foo@example.com")
            tool.set(data={})
            data = tool.get()
            self.assertEqual(data["email"], "foo@example.com")

    def test_set_ok_if_setter_user_is_admin(self):
        tool = self.get_tool(user=api.user.get(username="foo"))
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")
        tool.set(data={})
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")

    def test_do_not_set_fields_not_in_onceonly_fields(self):
        tool = self.get_tool(user=api.user.get(username="foo"))
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")
        tool.set(data={"xxx": "yyy"})
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")
        self.assertNotIn("xxx", data)

    def test_set_fields_in_onceonly_fields(self):
        service = api.content.create(
            type="Servizio", title="Servizio", container=api.portal.get()
        )
        mp = api.content.create(type="ModelloPratica", title="MP", container=service)
        mp.pratica_model = json.dumps({"pages": [{"elements": [{"valueName": "xxx"}]}]})

        # commit()

        tool = self.get_tool(user=api.user.get(username="foo"))
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")
        tool.set(data={"data": {"xxx": 123, "aaa": 456}, "form_id": mp.UID()})
        data = tool.get()
        self.assertEqual(data["email"], "foo@example.com")
        self.assertEqual(data["xxx"], 123)
        # TODO: se il dato non c'è, è più corretto "" o None ?
        self.assertEqual(data.get("yyy"), None)
        self.assertNotIn("aaa", data)
