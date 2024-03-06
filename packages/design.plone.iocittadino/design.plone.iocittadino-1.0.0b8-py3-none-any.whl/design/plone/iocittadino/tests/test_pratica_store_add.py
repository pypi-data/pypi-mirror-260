# -*- coding: utf-8 -*-
import datetime
import unittest

import freezegun
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

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperAdd(unittest.TestCase):
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

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )

        # add relation
        intids = getUtility(IIntIds)
        self.servizio.ufficio_responsabile = [RelationValue(intids.getId(self.ufficio))]

    def tearDown(self):
        self.tool.clear()

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_add_raise_error_if_missing_required_fields(self):
        self.assertEqual(self.tool.length, 0)

        self.assertRaises(ValueError, self.tool.add, {})
        self.assertEqual(self.tool.length, 0)

        self.assertRaises(ValueError, self.tool.add, {"form_id": ""})
        self.assertEqual(self.tool.length, 0)

        # also empty fields
        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": "", "data": ""},
        )
        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": "", "data": ""},
        )
        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": "bar", "data": ""},
        )

        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": self.modello_pratica.UID(), "data": ""},
        )

        self.tool.add({"form_id": self.modello_pratica.UID(), "data": "foo"})
        self.assertEqual(self.tool.length, 1)

    def test_add_raise_value_error_if_form_id_is_wrong(self):
        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": "foo", "data": ""},
        )

    def test_add_raise_error_if_missing_data_and_not_state_draft(self):
        self.assertRaises(
            ValueError,
            self.tool.add,
            {"form_id": self.modello_pratica.UID(), "data": ""},
        )
        self.assertRaises(
            ValueError,
            self.tool.add,
            {
                "form_id": self.modello_pratica.UID(),
                "data": "",
                "state": "xxx",
            },
        )

        self.assertEqual(self.tool.length, 0)
        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "",
                "state": "draft",
            }
        )
        self.assertEqual(self.tool.length, 1)

    def test_save_raise_error_if_state_different_from_draft(self):
        self.assertEqual(self.tool.length, 0)
        self.assertRaises(
            ValueError,
            self.tool.add,
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "state": "foo",
            },
        )

        self.assertEqual(self.tool.length, 0)
        self.tool.add({"form_id": self.modello_pratica.UID(), "data": "baz"})
        self.assertEqual(self.tool.length, 1)

    def test_correctly_add_data(self):
        self.assertEqual(self.tool.length, 0)
        self.tool.add({"form_id": self.modello_pratica.UID(), "data": "baz"})
        self.assertEqual(self.tool.length, 1)

    def test_save_only_store_defined_fields(self):
        self.assertEqual(self.tool.length, 0)
        record = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some value",
                "unknown_field": "mystery",
                "assigned_to": "jdoe",
            }
        )
        self.assertEqual(self.tool.length, 1)

        item = self.tool.get(record.intid)
        self.assertEqual(item.attrs.get("userid", None), api.user.get_current().getId())
        self.assertEqual(item.attrs.get("form_id", None), self.modello_pratica.UID())
        self.assertEqual(item.attrs.get("data", None), "some value")
        self.assertEqual(item.attrs.get("unknown_field", None), None)
        self.assertEqual(item.attrs.get("assigned_to", None), "jdoe")

    def test_add_create_record_with_related_servizio(self):
        record = self.tool.add({"form_id": self.modello_pratica.UID(), "data": "baz"})

        item = self.tool.get(record.intid)
        self.assertEqual(item.attrs.get("servizio", None), self.servizio.UID())

    def test_add_create_record_with_related_ufficio_from_servizio(self):
        record = self.tool.add({"form_id": self.modello_pratica.UID(), "data": "baz"})

        item = self.tool.get(record.intid)
        self.assertEqual(len(item.attrs.get("ufficio", [])), 1)
        self.assertEqual(item.attrs.get("ufficio", []), [self.ufficio.UID()])

    def test_ongoing_date_is_being_set_automatically_when_create(self):
        """If the item is being created with `ongoing` state, the ongoing date is being set automatically"""
        testing_time = datetime.datetime.utcnow()

        with freezegun.freeze_time(testing_time):
            record = self.tool.add(
                {
                    "form_id": self.modello_pratica.UID(),
                    "data": "some value",
                }
            )

        self.assertEquals(self.tool.get(record.intid).attrs.get("state"), "ongoing")
        self.assertEquals(
            self.tool.get(record.intid).attrs.get("ongoing_date"), testing_time
        )

    # TODO: check if tests below are working after the buildout fixes
    def test_send_mail_doesnt_sent_if_draft_creation(self):
        mailhost = self.portal.MailHost

        self.assertEqual(self.tool.length, 0)

        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "draft",
            }
        )

        # check email doesn send if created with a 'draft' state
        self.assertEqual(self.tool.length, 1)
        self.assertEqual(len(mailhost.messages), 0)

    def test_send_mail_send(self):
        mailhost = self.portal.MailHost
        self.assertEqual(self.tool.length, 0)

        # use user with email field
        with api.env.adopt_user(username="foo"):
            self.tool.add(
                {
                    "form_id": self.modello_pratica.UID(),
                    "data": "some data",
                    "state": "ongoing",
                }
            ).intid

        self.assertEqual(self.tool.length, 1)
        self.assertEqual(len(mailhost.messages), 1)

    def test_add_raise_error_if_there_is_another_pratica_in_draft_state_on_same_model(
        self,
    ):
        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
            }
        )
        self.assertEqual(self.tool.length, 1)

        with self.assertRaises(ValueError) as cm:
            self.tool.add(
                {
                    "form_id": self.modello_pratica.UID(),
                    "data": "another data",
                }
            )

        self.assertEqual(
            "Unable to submit a new Record. There is already a Record in progress for this Service.",
            str(cm.exception),
        )

    def test_add_raise_error_if_there_is_another_pratica_in_ongoing_state_on_same_model(
        self,
    ):
        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "ongoing",
            }
        )
        self.assertEqual(self.tool.length, 1)

        with self.assertRaises(ValueError) as cm:
            self.tool.add(
                {
                    "form_id": self.modello_pratica.UID(),
                    "data": "another data",
                }
            )

        self.assertEqual(
            "Unable to submit a new Record. There is already a Record in progress for this Service.",
            str(cm.exception),
        )

    def test_can_add_new_pratica_on_same_model_if_there_are_others_completed(
        self,
    ):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "ongoing",
            }
        ).intid
        self.tool.update_state(item_id=id, state="completed")

        self.assertEqual(self.tool.length, 1)

        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "another data",
            }
        )
        self.assertEqual(self.tool.length, 2)

    def test_can_add_new_pratica_on_same_model_if_there_are_others_suspended(
        self,
    ):
        id = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "ongoing",
            }
        ).intid
        self.tool.update_state(item_id=id, state="suspended")

        self.assertEqual(self.tool.length, 1)

        self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "another data",
            }
        )
        self.assertEqual(self.tool.length, 2)
