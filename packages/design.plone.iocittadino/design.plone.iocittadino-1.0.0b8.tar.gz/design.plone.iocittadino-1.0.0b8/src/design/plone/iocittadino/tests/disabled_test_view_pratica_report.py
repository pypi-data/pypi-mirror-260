# -*- coding: utf-8 -*-
import datetime
import unittest

import freezegun
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zExceptions import BadRequest
from zope.component import queryMultiAdapter

from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.testing import (  # noqa
    DESIGN_PLONE_IOCITTADINO_INTEGRATION_TESTING,
)


class DummyRelationObject:
    def __init__(self, object):
        self.object = object

    @property
    def to_object(self):
        return self.object


class DummyRelationField:
    def __init__(self, object):
        self.relation_object = DummyRelationObject(object)

    def __iter__(self):
        self.num = 0
        self.end = 1
        return self

    def __next__(self):
        if self.num >= self.end:
            raise StopIteration
        else:
            self.num += 1
            return self.relation_object


class TestViewPraticaReport(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.view = api.content.get_view(
            name="pratica_report", context=self.portal, request=self.request
        )
        self.pratica_storage = queryMultiAdapter(
            (api.portal.get(), self.request), IPraticaContentStore
        )
        self.uo = api.content.create(
            type="UnitaOrganizzativa",
            id="uo1",
            title="UO1",
            container=self.portal,
        )
        self.servizio = api.content.create(
            type="Servizio",
            id="servizio",
            title="Servizio",
            container=self.portal,
            ufficio_responsabile=DummyRelationField(self.uo),
        )
        self.modello_pratica = api.content.create(
            type="ModelloPratica",
            id="modello-pratica",
            title="Modello pratica",
            container=self.servizio,
        )
        self.pratica_datetime = datetime.datetime.now()
        pratica = {
            "form_id": self.modello_pratica.UID(),
            "numero_protocollo": "111",
            "state": "draft",
        }

        with freezegun.freeze_time(self.pratica_datetime):
            self.pratica = self.pratica_storage.add(pratica)

    def test_data_when_parameter_not_passed(self):
        """Tests data method whet `item_id` is not passed by request"""
        self.assertRaises(BadRequest, self.view.data)

    def test_unexistent_item_id(self):
        """Tests data method whet unexistent `item_id` is passed by request"""
        self.request["item_id"] = 123

        self.assertRaises(BadRequest, self.view.data)

    @unittest.skip("Da errori con il servizio")
    def test_positive(self):
        """Tests expected positive behavior of data method"""
        self.request["item_id"] = self.pratica

        with freezegun.freeze_time(self.pratica_datetime):
            self.pratica = self.pratica_storage.update_state(self.pratica, "ongoing")

        expected = {
            "form_id": self.modello_pratica.UID(),
            "numero_protocollo": "111",
            "servizio": self.servizio,
            "ufficio": self.uo,
            "title": self.modello_pratica.title,
            "creation_date": self.pratica_datetime.strftime("%m/%d/%Y"),
            "ongoing_date": self.pratica_datetime.strftime("%m/%d/%Y %H:%M:%S"),
        }
        for key, value in self.view.data().items():
            self.assertEqual(expected[key], value)
