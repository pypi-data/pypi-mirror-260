# -*- coding: utf-8 -*-
import json
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from design.plone.iocittadino.content.modello_pratica import IModelloPratica
from design.plone.iocittadino.exceptions import InvalidEmailError
from design.plone.iocittadino.interfaces.modello_pratica import isEmail
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class ModelloPraticaIntegrationTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Servizio",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_modello_pratica_schema(self):
        fti = queryUtility(IDexterityFTI, name="ModelloPratica")
        schema = fti.lookupSchema()
        self.assertEqual(IModelloPratica, schema)

    def test_ct_modello_pratica_fti(self):
        fti = queryUtility(IDexterityFTI, name="ModelloPratica")
        self.assertTrue(fti)

    def test_ct_modello_pratica_factory(self):
        fti = queryUtility(IDexterityFTI, name="ModelloPratica")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IModelloPratica.providedBy(obj),
            "IModelloPratica not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_modello_pratica_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="ModelloPratica",
            id="modello_pratica",
        )

        self.assertTrue(
            IModelloPratica.providedBy(obj),
            "IModelloPratica not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("modello_pratica", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("modello_pratica", parent.objectIds())

    def test_ct_modello_pratica_using_model(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="ModelloPratica",
            title="Assegno di Maternità",
            model="assegno_maternita.json",
        )
        self.assertEqual(
            json.loads(obj.pratica_model)["title"],
            "Assegno di maternità",
        )

    def test_ct_modello_pratica_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="ModelloPratica")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))

    def test_is_email(self):
        self.assertTrue(isEmail("mario.rossi@example.org"))
        self.assertRaises(InvalidEmailError, isEmail, "mario rossi")
        self.assertRaises(InvalidEmailError, isEmail, "mario.rossi")
