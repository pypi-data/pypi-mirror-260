# -*- coding: utf-8 -*-
from plone import api
from transaction import commit

from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiListing(Mixin):
    def test_listing_need_to_be_called_on_root(self):
        resp = self.api_session_manager.get(
            f"{self.servizio.absolute_url()}/@pratiche",
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.get(
            f"{self.modello_pratica.absolute_url()}/@pratiche",
        )
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratiche",
        )
        self.assertEqual(resp.status_code, 200)

    def test_listing_by_default_return_summary_pratica_data(self):
        self.api_session_manager.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratiche",
        ).json()

        self.assertNotIn("data", resp["items"][0].keys())

    def test_listing_return_expanded_data_if_needed(self):
        self.api_session_manager.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        resp = self.api_session_manager.get(
            f"{self.portal_url}/@pratiche?fullobjects=1",
        ).json()

        self.assertIn("data", resp["items"][0].keys())
        self.assertIn("form", resp["items"][0].keys())

    def test_anon_cant_get_data(self):
        resp = self.api_session_anon.get(
            f"{self.portal_url}/@pratiche",
        )
        self.assertEqual(resp.status_code, 401)

    def test_simple_users_cant_get_record_from_other_users(self):
        self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        self.api_session_other.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from other",
            },
        )

        # auth can only see his record
        res = self.api_session_auth.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 1)
        self.assertEqual(res["items"][0]["userid"], "foo")

        # other can only see his record
        res = self.api_session_other.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 1)
        self.assertEqual(res["items"][0]["userid"], "bar")

        # gestori can see both
        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "bar")
        self.assertEqual(res["items"][1]["userid"], "foo")

    def test_power_users_can_filter_by_userid(self):
        self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        self.api_session_other.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from other",
            },
        )

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 2)

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche?userid=foo"
        ).json()
        self.assertEqual(res["items_total"], 1)
        self.assertEqual(res["items"][0]["userid"], "foo")

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche?userid=bar"
        ).json()
        self.assertEqual(res["items_total"], 1)
        self.assertEqual(res["items"][0]["userid"], "bar")

    def test_gestore_cant_get_record_from_modelli_that_cant_access(self):
        modello_pratica_private = api.content.create(
            type="ModelloPratica",
            id="private-modello",
            title="Private Modello",
            container=self.servizio,
            pratica_model="foo schema",
        )
        commit()

        self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        self.api_session_manager.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": modello_pratica_private.UID(),
                "data": "data private",
            },
        )

        # admin can see both
        res = self.api_session_manager.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 2)

        # gestor2 can see only public one
        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 1)
        self.assertEqual(
            res["items"][0]["form"]["id"],
            self.modello_pratica.getId(),
        )

    def test_pratiche_endpoint_return_list_of_unique_services(self):
        self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        )

        self.api_session_other.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from other",
            },
        )

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@pratiche",
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertIn("services", res)
        self.assertEqual(len(res["services"]), 1)
        self.assertEqual(res["services"][0]["@id"], self.servizio.absolute_url())
