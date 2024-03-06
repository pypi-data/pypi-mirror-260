# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from z3c.relationfield import RelationValue
from zExceptions import Unauthorized
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestSouperPatch(unittest.TestCase):
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

        # add relation
        intids = getUtility(IIntIds)
        self.servizio.ufficio_responsabile = [RelationValue(intids.getId(self.ufficio))]

        self.pratica_id = self.pratica_storage.add(
            {"form_id": self.modello_pratica.UID(), "data": "some data"}
        ).intid
        self.message_id = self.message_storage.add(
            {"pratica_id": self.pratica_id, "message": "message"}
        )

    def tearDown(self):
        self.message_storage.clear()
        self.pratica_storage.clear()

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_update_record_return_error_if_id_not_passed(self):
        self.assertRaises(
            Unauthorized,
            self.message_storage.update,
            self.message_id,
            {},
        )
