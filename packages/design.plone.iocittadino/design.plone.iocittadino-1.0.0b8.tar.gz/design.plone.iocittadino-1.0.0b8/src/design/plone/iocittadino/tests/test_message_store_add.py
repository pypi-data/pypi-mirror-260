# -*- coding: utf-8 -*-
import base64
import io
import unittest

from Acquisition import aq_base
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


def generate_dummy_stream(size=1):
    return io.BytesIO(b"\0" * size).read()


class TestSouperMessageAdd(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost("MailHost")
        api.portal.set_registry_record(
            "plone.email_from_address", "noreply@holokinesislibros.com"
        )
        sm = getSiteManager(context=self.portal)

        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # create contents
        self.servizio = api.content.create(
            type="Servizio",
            id="example-service",
            title="Example Service",
            container=self.portal,
        )

        self.ufficio = api.content.create(
            type="UnitaOrganizzativa",
            id="example-uo",
            title="Example UO",
            container=self.portal,
        )
        self.modello_pratica = api.content.create(
            type="ModelloPratica",
            id="example-modello",
            title="Example Modello",
            container=self.servizio,
        )

        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.ufficio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")

        # add relation
        intids = getUtility(IIntIds)
        self.servizio.ufficio_responsabile = [RelationValue(intids.getId(self.ufficio))]

        self.pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
            }
        ).intid

        # create an user with email
        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )

    def tearDown(self):
        self.pratica_storage.clear()
        self.message_storage.clear()

        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost), provided=IMailHost)

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    @property
    def message_text(self):
        """Testin message text"""
        return "Testing message"

    def test_add_raise_error_if_missing_required_fields(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)

        self.assertRaises(ValueError, self.message_storage.add, {})
        self.assertEqual(self.message_storage.length, 1)

        self.assertRaises(ValueError, self.message_storage.add, {"pratica_id": ""})
        self.assertEqual(self.message_storage.length, 1)

        # also empty fields
        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {"pratica_id": "", "message": ""},
        )
        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {"pratica_id": "", "message": ""},
        )
        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {"pratica_id": "bar", "message": ""},
        )

        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {"pratica_id": self.pratica_id, "message": ""},
        )

        self.message_storage.add({"pratica_id": self.pratica_id, "message": "foo"})
        self.assertEqual(self.message_storage.length, 2)

    def test_add_raise_value_error_if_form_id_is_wrong(self):
        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {"pratica_id": "foo", "message": ""},
        )

    def test_email_sent_on_message_creation(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)
        self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
                "state": "sent",
            }
        )
        self.assertEqual(self.message_storage.length, 2)

    def test_save_raise_error_if_state_different_from_allowed(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)

        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
                "state": "foo",
            },
        )

        self.assertEqual(self.message_storage.length, 1)
        self.message_storage.add({"pratica_id": self.pratica_id, "message": "message"})
        self.assertEqual(self.message_storage.length, 2)

    def test_correctly_add_data(self):
        self.assertEqual(self.message_storage.length, 1)
        self.message_storage.add({"pratica_id": self.pratica_id, "message": "message"})
        self.assertEqual(self.message_storage.length, 2)

    def test_save_only_store_defined_fields(self):
        self.assertEqual(self.message_storage.length, 1)
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
                "unknown_field": "mystery",
            }
        ).intid
        self.assertEqual(self.message_storage.length, 2)

        item = self.message_storage.get(id)
        self.assertEqual(item.attrs.get("userid", None), api.user.get_current().getId())
        self.assertEqual(item.attrs.get("pratica_id", None), self.pratica_id)
        self.assertEqual(item.attrs.get("message", None), self.message_text)
        self.assertEqual(item.attrs.get("unknown_field", None), None)

    def test_object_uid_relation(self):
        ob = api.content.create(
            type="Document", title="Tester", container=api.portal.get()
        )
        id = self.message_storage.add(
            {
                "object_uid": ob.UID(),
                "message": self.message_text,
            }
        ).intid

        self.assertTrue(self.message_storage.get(id))

    def test_no_relation_provided(self):
        with self.assertRaises(ValueError) as err:
            self.message_storage.add(
                {
                    "message": self.message_text,
                }
            )

        self.assertEqual(
            "Must be provided `pratica_id` or `object_uid` parameter",
            str(err.exception),
        )

    def test_attachments_max_size_negative(self):
        from design.plone.iocittadino.adapters.content_store.message import (
            MESSAGE_ATTACHMENTS_FILESIZE_MAX,
        )

        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
                "attachments": [
                    {
                        "name": "test.txt",
                        "data": f"data:application/pdf;base64,${base64.b64encode(generate_dummy_stream(MESSAGE_ATTACHMENTS_FILESIZE_MAX + 1))}",  # noqa
                    }
                ],
            },
        )

    def test_attachments_max_size_ok(self):
        id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
                "attachments": [
                    {
                        "name": "test.txt",
                        "data": f"data:application/pdf;base64,${base64.b64encode(generate_dummy_stream(1024))}",  # noqa
                    }
                ],
            }
        ).intid
        self.assertTrue(self.message_storage.get(id))

    def test_attachments_bad_encoding(self):
        self.assertRaises(
            ValueError,
            self.message_storage.add,
            {
                "pratica_id": self.pratica_id,
                "message": "some value",
                "attachments": [
                    {
                        "name": "test.txt",
                        "data": "data:application/pdf;base64,bad encoded",
                    }
                ],
            },
        )
