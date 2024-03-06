# -*- coding: utf-8 -*-
import unittest
from email import message_from_string

from Acquisition import aq_base
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
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

    def test_do_not_send_mail_on_creation_if_not_email(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)
        # TODO: modificare add da un metodo che accetta un dict a uno che accetta
        #       singoli parametri, ed eventualmente un kwargs
        self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
            }
        )

        mailhost = self.portal.MailHost
        # 1 so as we have already email about pratica creation
        self.assertEqual(len(mailhost.messages), 0)

    def test_send_mail_on_creation(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)
        logout()

        login(self.portal, "foo")
        new_pratica = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data from foo",
            }
        ).intid

        login(self.portal, TEST_USER_NAME)
        # TODO: modificare add da un metodo che accetta un dict a uno che accetta
        #       singoli parametri, ed eventualmente un kwargs
        self.message_storage.add(
            {
                "pratica_id": new_pratica,
                "message": self.message_text,
            }
        )

        mailhost = self.portal.MailHost

        # 2 because there is also the pratica message
        self.assertEqual(len(mailhost.messages), 2)
        msg = message_from_string(mailhost.messages[1].decode())
        body = msg.get_payload()
        self.assertIn(self.message_text, body[0].get_payload())

    def test_do_not_send_mail_on_creation_if_not_flag(self):
        # 1 so as we have already email about pratica creation
        self.assertEqual(self.message_storage.length, 1)

        logout()
        login(self.portal, "foo")
        new_pratica = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data from foo",
            }
        ).intid
        login(self.portal, TEST_USER_NAME)

        self.message_storage.add(
            {
                "pratica_id": new_pratica,
                "message": self.message_text,
                "notify_on_email": False,
            }
        )

        mailhost = self.portal.MailHost

        # 1 because there is also the pratica message
        self.assertEqual(len(mailhost.messages), 1)
