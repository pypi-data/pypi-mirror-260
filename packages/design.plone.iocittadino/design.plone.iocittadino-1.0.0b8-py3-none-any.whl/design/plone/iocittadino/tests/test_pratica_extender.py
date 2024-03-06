# -*- coding: utf-8 -*-
# import datetime
import unittest

# import freezegun
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

# from z3c.relationfield import RelationValue
from zope import interface
from zope.component import getMultiAdapter
from zope.component import getSiteManager

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaStoreFieldsExtender
from design.plone.iocittadino.interfaces import IPraticaStoreSerializerExtender
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

# from zope.component import getUtility
# from zope.intid.interfaces import IIntIds


@interface.implementer(IPraticaStoreFieldsExtender)
class FieldExtender(object):
    @property
    def fields(self):
        return {
            "new_field_a": {"required": False},
            "new_field_b": {"required": False},
            "new_field_c": {"required": False},
        }


@interface.implementer(IPraticaStoreSerializerExtender)
class ExtendsPraticaSerializer(object):
    def get_fields(self, pratica):
        return {
            "new_field_a": "A_value",
            "new_field_b": "B_value",
            "new_field_c": "C_value",
        }


class TestPraticaExtender(unittest.TestCase):
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

        self.modello_pratica = api.content.create(
            type="ModelloPratica",
            id="example-modello",
            title="Example Modello",
            container=self.servizio,
        )

        # register utility for file extension
        sm.registerUtility(
            FieldExtender(), name="field_extender", provided=IPraticaStoreFieldsExtender
        )
        sm.registerUtility(
            ExtendsPraticaSerializer(),
            name="serializer_extender",
            provided=IPraticaStoreSerializerExtender,
        )

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_extended_fields(self):
        fields = self.tool.fields
        self.assertIn("new_field_a", fields)
        self.assertIn("new_field_b", fields)
        self.assertIn("new_field_c", fields)

    def test_extended_serializer(self):
        pratica = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "ongoing",
            }
        )
        result = getMultiAdapter((pratica, self.request), ISerializePraticaToJson)()
        self.assertIn("new_field_a", result)
        self.assertIn("new_field_b", result)
        self.assertIn("new_field_c", result)
