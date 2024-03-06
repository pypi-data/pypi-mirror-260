# -*- coding: utf-8 -*-
from plone import api
from transaction import commit

from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiListing(Mixin):
    def test_listing_need_to_be_called_on_root(self):
        resp = self.api_session_manager.get(
            f"{self.servizio.absolute_url()}/@messages",
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.get(
            f"{self.modello_pratica.absolute_url()}/@message",
        )
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@messages",
        )
        self.assertEqual(resp.status_code, 200)

    def test_anon_cant_get_data(self):
        resp = self.api_session_anon.get(
            f"{self.portal_url}/@messages",
        )
        self.assertEqual(resp.status_code, 401)

    def test_simple_users_cant_get_record_from_other_users(self):
        pratica_auth_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_auth_id,
                "message": "message",
            },
        )

        pratica_other_id = self.api_session_other.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_other_id,
                "message": "message1",
            },
        )

        # auth can only see his record
        res = self.api_session_auth.get(
            f"{self.portal_url}/@messages",
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "foo")
        self.assertEqual(res["items"][0]["message"], "message")

        # other can only see his record
        res = self.api_session_other.get(
            f"{self.portal_url}/@messages",
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "bar")
        self.assertEqual(res["items"][0]["message"], "message1")

        # gestore can see both
        res = self.api_session_gestore.get(
            f"{self.portal_url}/@messages",
        ).json()

        self.assertEqual(res["items_total"], 4)
        self.assertEqual(res["items"][0]["userid"], "bar")
        self.assertEqual(res["items"][0]["message"], "message1")
        self.assertEqual(res["items"][2]["userid"], "foo")
        self.assertEqual(res["items"][2]["message"], "message")

    def test_simple_users_can_get_record_from_private_modello_pratica(self):
        other_pratica = api.content.create(
            type="ModelloPratica",
            id="other-modello",
            title="Other Modello",
            container=self.servizio,
            pratica_model="foo schema",
        )
        api.content.transition(obj=other_pratica, transition="publish")
        commit()

        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": other_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_id,
                "message": "message",
            },
        )

        api.content.transition(obj=other_pratica, transition="retract")
        commit()

        resp = self.api_session_auth.get(
            f"{self.portal_url}/@messages",
        )
        res = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "foo")
        self.assertEqual(res["items"][0]["message"], "message")

    def test_power_users_can_filter_by_userid(self):
        pratica_auth_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_auth_id,
                "message": "message",
            },
        )

        pratica_other_id = self.api_session_other.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_other_id,
                "message": "message1",
            },
        )

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@messages",
        ).json()
        self.assertEqual(res["items_total"], 4)

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@messages?userid=foo"
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "foo")

        res = self.api_session_gestore.get(
            f"{self.portal_url}/@messages?userid=bar"
        ).json()
        self.assertEqual(res["items_total"], 2)
        self.assertEqual(res["items"][0]["userid"], "bar")
