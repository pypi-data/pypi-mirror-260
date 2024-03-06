# -*- coding: utf-8 -*-
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiDelete(Mixin):
    def test_delete_can_called_only_on_root(self):
        resp = self.api_session_manager.delete(
            f"{self.servizio.absolute_url()}/@pratica",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.delete(
            f"{self.modello_pratica.absolute_url()}/@pratica",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_return_404_if_no_id_passed(self):
        resp = self.api_session_manager.delete(f"{self.portal_url}/@pratica")

        self.assertEqual(resp.status_code, 404)

    def test_delete_return_404_if_invalid_id_passed(self):
        resp = self.api_session_manager.delete(f"{self.portal_url}/@pratica/foo")

        self.assertEqual(resp.status_code, 400)

    def test_delete_return_200_if_ok(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
                "state": "draft",
            },
        ).json()["item_id"]

        self.assertEqual(self.get_pratica_records()["items_total"], 1)

        resp = self.api_session_manager.delete(
            f"{self.portal_url}/@pratica/{pratica_id}"
        )

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.get_pratica_records()["items_total"], 0)

    def test_simple_user_can_delete_its_record(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
                "state": "draft",
            },
        ).json()["item_id"]

        self.assertEqual(self.get_pratica_records()["items_total"], 1)

        resp = self.api_session_auth.delete(f"{self.portal_url}/@pratica/{pratica_id}")

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.get_pratica_records()["items_total"], 0)

    def test_simple_user_cant_delete_other_users_records(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
                "state": "draft",
            },
        ).json()["item_id"]

        self.assertEqual(self.get_pratica_records()["items_total"], 1)

        resp = self.api_session_other.delete(f"{self.portal_url}/@pratica/{pratica_id}")

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(self.get_pratica_records()["items_total"], 1)

    def test_gestore_can_delete_other_users_records(self):
        pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "data from auth",
                "state": "draft",
            },
        ).json()["item_id"]

        self.assertEqual(self.get_pratica_records()["items_total"], 1)

        resp = self.api_session_gestore.delete(
            f"{self.portal_url}/@pratica/{pratica_id}"
        )

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.get_pratica_records()["items_total"], 0)
