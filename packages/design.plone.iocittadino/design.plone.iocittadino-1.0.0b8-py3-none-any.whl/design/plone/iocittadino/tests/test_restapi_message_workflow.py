# -*- coding: utf-8 -*-
from transaction import commit

from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiPraticaWorkflow(Mixin):
    def setUp(self):
        super().setUp()
        self.pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "data": "foo"},
        ).json()["item_id"]

        self.message_id = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": self.pratica_id, "message": "message"},
        ).json()["item_id"]

        commit()

    def test_endpoint_can_called_only_on_root(self):
        resp = self.api_session_manager.post(
            f"{self.servizio.absolute_url()}/@message-workflow/{self.message_id}",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.post(
            f"{self.modello_pratica.absolute_url()}/@message-workflow/{self.message_id}",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message-workflow/{self.message_id}",
            json={},
        )
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 400)

    def test_endpoint_return_404_if_message_id_not_passed(self):
        resp = self.api_session_manager.post(
            f"{self.portal_url}/@message-workflow", json={}
        )
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 400)

    def test_endpoint_required_data(self):
        resp = self.api_session_manager.post(
            f"{self.portal_url}/@message-workflow/{self.message_id}", json={}
        )

        self.assertEqual(resp.status_code, 400)
        # self.assertEqual(resp.json()["message"], 'Missing "state" field.')

        resp = self.api_session_manager.post(
            f"{self.portal_url}/@message-workflow/{self.message_id}",
            json={"state": ""},
        )
        self.assertEqual(resp.status_code, 400)
        # self.assertEqual(resp.json()["message"], 'Missing "state" field.')

    def test_passing_wrong_message_id_return_404(self):
        resp = self.api_session_manager.post(
            f"{self.portal_url}/@message-workflow/foo", json={"state": "bar"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_endpoint_success(self):
        record = self.api_session_manager.get(
            f"{self.portal_url}/@message/{self.message_id}",
        ).json()
        self.assertEqual(record["state"], "pending")

        resp = self.api_session_manager.post(
            f"{self.portal_url}/@message-workflow/{self.message_id}",
            json={"state": "sent"},
        )

        self.assertEqual(resp.status_code, 204)
