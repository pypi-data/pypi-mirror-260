# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope import component
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import ISerializePraticaToJson
from design.plone.iocittadino.interfaces import ISerializePraticaToJsonSummary
from design.plone.iocittadino.testing import DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING


class TestPraticaSerializer(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

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

    @property
    def tool(self):
        return getMultiAdapter((self.portal, self.request), IPraticaContentStore)

    def test_serializer_return_data_and_form_infos(self):
        draft = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "draft",
            }
        )
        result = component.getMultiAdapter(
            (draft, self.request), ISerializePraticaToJson
        )()

        self.assertIn("data", result.keys())

    def test_summary_serializer_do_not_return_data_and_form_infos(self):
        draft = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "form": "form data",
                "state": "draft",
            }
        )
        result = component.getMultiAdapter(
            (draft, self.request), ISerializePraticaToJsonSummary
        )()

        self.assertNotIn("data", result.keys())

    def test_serializer_return_next_states_from_draft(self):
        pratica = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "draft",
            }
        )
        result = component.getMultiAdapter(
            (pratica, self.request), ISerializePraticaToJson
        )()

        self.assertEqual(result["state"], "draft")
        self.assertEqual(result["available_states"], ["ongoing", "canceled"])

    def test_serializer_return_next_states_from_ongoing(self):
        pratica = self.tool.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "some data",
                "state": "ongoing",
            }
        )
        result = component.getMultiAdapter(
            (pratica, self.request), ISerializePraticaToJson
        )()
        self.assertEqual(result["state"], "ongoing")
        self.assertEqual(
            result["available_states"],
            ["suspended", "completed", "canceled", "draft"],
        )


def test_serializer_return_next_states_from_suspended(self):
    pratica = self.tool.add(
        {
            "form_id": self.modello_pratica.UID(),
            "data": "some data",
            "state": "ongoing",
        }
    )
    self.tool.update_state(item_id=pratica.intid, state="suspended")
    result = component.getMultiAdapter(
        (pratica, self.request), ISerializePraticaToJson
    )()
    self.assertEqual(result["state"], "suspended")
    self.assertEqual(result["available_states"], ["ongoing", "completed", "canceled"])


def test_serializer_return_next_states_from_completed(self):
    pratica = self.tool.add(
        {
            "form_id": self.modello_pratica.UID(),
            "data": "some data",
            "state": "ongoing",
        }
    )
    self.tool.update_state(item_id=pratica.intid, state="completed")
    result = component.getMultiAdapter(
        (pratica, self.request), ISerializePraticaToJson
    )()
    self.assertEqual(result["state"], "completed")
    self.assertEqual(result["available_states"], [])
