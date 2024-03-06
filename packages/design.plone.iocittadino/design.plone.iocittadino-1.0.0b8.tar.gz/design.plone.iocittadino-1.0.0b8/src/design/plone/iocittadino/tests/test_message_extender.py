# -*- coding: utf-8 -*-
# import datetime
import base64

import transaction
from pkg_resources import resource_string

# from z3c.relationfield import RelationValue
from zope import interface
from zope.component import getMultiAdapter
from zope.component import getSiteManager

from design.plone.iocittadino.interfaces import IMessageContentStore
from design.plone.iocittadino.interfaces import IMessageStoreFieldsExtender
from design.plone.iocittadino.interfaces import IMessageStoreSerializerExtender
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.tests.restapi_mixin import Mixin

PDF_B64 = base64.b64encode(
    resource_string("design.plone.iocittadino.tests", "dummy.pdf")
)


@interface.implementer(IMessageStoreFieldsExtender)
class FieldExtender(object):
    @property
    def fields(self):
        return {
            "new_field_a": {"required": False},
            "new_field_b": {"required": False},
            "new_field_c": {"required": False},
        }


@interface.implementer(IMessageStoreSerializerExtender)
class ExtendsMessageSerializer(object):
    def get_fields(self, pratica):
        return {
            "new_field_a": "A_value",
            "new_field_b": "B_value",
            "new_field_c": "C_value",
        }


class TestPraticaExtender(Mixin):
    # layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        sm = getSiteManager(context=self.portal)
        self.pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
            }
        ).intid

        self.message_initial_state = "pending"
        self.message_text = "Testing message"
        self.message_id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
                "attachments": [
                    {
                        "name": "dummy.txt",
                        "data": "data:plain/text;base64,ZHVtbXkgdGV4dCBmaWxl",
                    },
                    {
                        "name": "dummy.pdf",
                        "data": f"data:application/pdf;base64,${PDF_B64}",
                    },
                ],
            }
        ).intid

        # register utility for file extension
        sm.registerUtility(
            FieldExtender(), name="field_extender", provided=IMessageStoreFieldsExtender
        )
        sm.registerUtility(
            ExtendsMessageSerializer(),
            name="serializer_extender",
            provided=IMessageStoreSerializerExtender,
        )
        transaction.commit()

    @property
    def pratica_storage(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    @property
    def message_storage(self):
        return getMultiAdapter((self.portal, self.request), IMessageContentStore)

    def test_extended_fields(self):
        fields = self.message_storage.fields
        self.assertIn("new_field_a", fields)
        self.assertIn("new_field_b", fields)
        self.assertIn("new_field_c", fields)

    def test_get_return_serialized_data(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        self.assertEqual(res["new_field_a"], "A_value")
        self.assertEqual(res["new_field_b"], "B_value")
        self.assertEqual(res["new_field_c"], "C_value")
