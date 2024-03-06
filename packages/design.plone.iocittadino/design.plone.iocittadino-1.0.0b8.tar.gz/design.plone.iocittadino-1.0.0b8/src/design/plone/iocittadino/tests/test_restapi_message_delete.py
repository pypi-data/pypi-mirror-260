# -*- coding: utf-8 -*-
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiDelete(Mixin):
    def test_delete_can_called_only_on_root(self):
        resp = self.api_session_manager.delete(
            f"{self.servizio.absolute_url()}/@message",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.delete(
            f"{self.modello_pratica.absolute_url()}/@message",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_return_404_if_no_id_passed(self):
        resp = self.api_session_manager.delete(f"{self.portal_url}/@message")

        self.assertEqual(resp.status_code, 404)

    def test_delete_return_404_if_invalid_id_passed(self):
        resp = self.api_session_manager.delete(f"{self.portal_url}/@message/foo")

        self.assertEqual(resp.status_code, 400)

    def test_efitor_delete_return_200_if_ok(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        message_id = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": pratica_id, "message": "message"},
        ).json()["item_id"]

        self.assertEqual(self.get_message_records()["items_total"], 2)

        resp = self.api_session_gestore.delete(
            f"{self.portal_url}/@message/{message_id}"
        )

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.get_message_records()["items_total"], 1)

    def test_simple_user_cant_delete_a_record(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
            },
        ).json()["item_id"]

        message_id = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": pratica_id, "message": "message"},
        ).json()["item_id"]

        self.assertEqual(self.get_pratica_records()["items_total"], 1)

        resp = self.api_session_auth.delete(f"{self.portal_url}/@message/{message_id}")

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(self.get_message_records()["items_total"], 2)
