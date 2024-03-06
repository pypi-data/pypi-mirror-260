# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.restapi.testing import RelativeSession
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import (
    DESIGN_PLONE_IOCITTADINO_API_FUNCTIONAL_TESTING,
)


# TODO: spostare su un layer ?
class Mixin(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session_manager = RelativeSession(self.portal_url)
        self.api_session_manager.headers.update({"Accept": "application/json"})
        self.api_session_manager.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.api_session_anon = RelativeSession(self.portal_url)
        self.api_session_anon.headers.update({"Accept": "application/json"})

        api.user.create(
            email="foo@example.com",
            username="foo",
            password="secret123",
        )
        api.user.create(
            email="bar@example.com",
            username="bar",
            password="secret123",
        )

        api.user.create(
            email="gestore@example.com",
            username="gestore",
            password="secret123",
        )
        setRoles(self.portal, "gestore", ["Gestore Pratiche"])

        self.api_session_auth = RelativeSession(self.portal_url)
        self.api_session_auth.headers.update({"Accept": "application/json"})
        self.api_session_auth.auth = ("foo", "secret123")

        self.api_session_other = RelativeSession(self.portal_url)
        self.api_session_other.headers.update({"Accept": "application/json"})
        self.api_session_other.auth = ("bar", "secret123")

        self.api_session_gestore = RelativeSession(self.portal_url)
        self.api_session_gestore.headers.update({"Accept": "application/json"})
        self.api_session_gestore.auth = ("gestore", "secret123")

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
            pratica_model="foo schema",
        )

        # add relation
        intids = getUtility(IIntIds)
        self.servizio.ufficio_responsabile = [RelationValue(intids.getId(self.ufficio))]

        api.content.transition(obj=self.servizio, transition="publish")
        api.content.transition(obj=self.modello_pratica, transition="publish")
        api.content.transition(obj=self.ufficio, transition="publish")

        transaction.commit()

    def tearDown(self) -> None:
        self.api_session_manager.close()
        self.api_session_anon.close()
        self.api_session_auth.close()
        self.api_session_other.close()
        self.api_session_gestore.close()
        self.pratica_storage.clear()

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    def get_pratica_records(self):
        resp = self.api_session_manager.get(f"{self.portal_url}/@pratiche")
        return resp.json()

    def get_message_records(self):
        resp = self.api_session_manager.get(f"{self.portal_url}/@messages")
        return resp.json()
