# -*- coding: utf-8 -*-
import json

from plone import api
from transaction import commit
from zope.component import getMultiAdapter

from design.plone.iocittadino.interfaces import IUserStore
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiGet(Mixin):
    def test_get_need_to_be_called_on_root(self):
        resp = self.api_session_manager.get(
            f"{self.servizio.absolute_url()}/@pratica",
        )
        self.assertEqual(resp.status_code, 404)
        resp = self.api_session_manager.get(
            f"{self.modello_pratica.absolute_url()}/@pratica",
        )
        self.assertEqual(resp.status_code, 404)

    def test_get_return_defaults(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratica",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["id"], "admin")

    def test_get_return_defaults_with_onceonly_fields_if_set(self):
        resp = self.api_session_auth.get(
            f"{self.portal_url}/@pratica",
        )
        self.assertEqual(resp.json()["data"]["id"], "foo")
        self.assertEqual(resp.json()["data"]["email"], "foo@example.com")
        self.assertNotIn("xxx", resp.json()["data"])
        self.assertNotIn("aaa", resp.json()["data"])

        self.modello_pratica.pratica_model = json.dumps(
            {"pages": [{"elements": [{"valueName": "xxx"}]}]}
        )

        commit()
        with api.env.adopt_user(username="foo"):
            tool = getMultiAdapter(
                (self.portal, api.user.get_current(), self.request), IUserStore
            )
            tool.set(
                data={
                    "data": {"xxx": 123, "aaa": 456},
                    "form_id": self.modello_pratica.UID(),
                }
            )
            commit()

        resp = self.api_session_auth.get(
            f"{self.portal_url}/@pratica",
        )
        self.assertEqual(resp.json()["data"]["id"], "foo")
        self.assertEqual(resp.json()["data"]["email"], "foo@example.com")
        self.assertEqual(resp.json()["data"]["xxx"], 123)
        self.assertNotIn("aaa", resp.json()["data"])

    def test_get_return_bad_request_for_wrong_id_type(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratica/foo",
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_return_not_found_wrong_id(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratica/0000",
        )
        self.assertEqual(resp.status_code, 404)

    def test_get_return_serialized_data(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()

        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        self.assertEqual(res["item_id"], pratica_id)
        self.assertEqual(res["userid"], api.user.get_current().getId())
        self.assertEqual(res["data"], "a value")
        self.assertEqual(res["state"], "ongoing")
        self.assertEqual(res["assigned_to"], "jdoe")
        self.assertIn("creation_date", res.keys())

    def test_anon_cant_get_data(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_anon.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        )
        self.assertEqual(resp.status_code, 401)

    def test_users_cant_get_record_from_other_users(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_auth.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        )
        self.assertEqual(resp.status_code, 401)

    def test_gestori_can_get_record(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        self.assertEqual(res["item_id"], pratica_id)
        self.assertEqual(res["userid"], api.user.get_current().getId())
        self.assertEqual(res["data"], "a value")
        self.assertEqual(res["state"], "ongoing")
        self.assertIn("creation_date", res.keys())

    def test_get_return_serialized_servizio(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        ).json()

        self.assertIn("servizio", resp.keys())
        self.assertEqual(resp["servizio"]["title"], self.servizio.Title())
        self.assertIn("form", resp.keys())
        self.assertEqual(resp["form"]["title"], self.modello_pratica.Title())

    def test_get_return_serialized_ufficio(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        ).json()

        self.assertIn("ufficio", resp.keys())
        self.assertEqual(len(resp["ufficio"]), 1)
        self.assertEqual(resp["ufficio"][0]["title"], self.ufficio.Title())

    def test_get_return_available_states_based_on_pratica_state(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        ).json()

        self.assertEqual(resp["state"], "ongoing")
        self.assertEqual(
            resp["available_states"],
            ["suspended", "completed", "canceled", "draft"],
        ),

    def test_pratica_does_not_have_report(self):
        pratica = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        )
        pratica_id = pratica.intid

        self.pratica_storage.store.update(
            pratica_id, {**pratica.attrs, "pratica_report": None}
        )

        commit()

        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        ).json()

        self.assertFalse(resp["has_report"])

    def test_pratica_has_report(self):
        pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "assigned_to": "jdoe",
            }
        ).intid

        commit()

        # The report shoul be created automaticaly
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica_id}",
        ).json()

        self.assertTrue(resp["has_report"])

    def test_pratica_return_data_and_form_by_default(self):
        pratica = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "form": "foo",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{pratica}",
        ).json()
        self.assertIn("data", resp.keys())
        self.assertIn("form", resp.keys())

    def test_pratica_return_data_and_form_by_default_search_by_form_id(self):
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": {"key": "value"},
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["state"], "ongoing")
        self.assertEqual(resp.json()["data"], {"key": "value"})
        item_id = resp.json()["item_id"]
        # query by form_id for the same user returns the saved data
        resp = self.api_session_auth.get(
            f"{self.portal_url}/@pratica/?form_id={self.modello_pratica.UID()}",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(item_id, resp.json()["item_id"])
        self.assertEqual(resp.json()["state"], "ongoing")
        self.assertEqual(resp.json()["data"], {"key": "value"})
        # the same query for a different user returns default data
        resp = self.api_session_other.get(
            f"{self.portal_url}/@pratica/?form_id={self.modello_pratica.UID()}",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("item_id", resp.json())
        self.assertEqual(resp.json()["data"]["email"], "bar@example.com")
        self.assertEqual(resp.json()["data"]["id"], "bar")

    def test_pratica_return_summarized_form_by_default(self):
        item_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "form": "foo",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{item_id}",
        ).json()
        self.assertNotIn("pratica_model", resp["form"])

    def test_pratica_return_form_schema_if_required(self):
        item_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
                "form": "foo",
            }
        ).intid
        commit()
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@pratica/{item_id}?show_schema=1",
        ).json()
        self.assertIn("pratica_model", resp["form"])
        self.assertEqual(
            resp["form"]["pratica_model"], self.modello_pratica.pratica_model
        )
