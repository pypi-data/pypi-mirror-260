# -*- coding: utf-8 -*-
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiAdd(Mixin):
    def submit(self, api_session, url, data):
        resp = api_session.post(
            f"{url}/@add-record",
            json=data,
        )
        return resp

    def test_add_record_can_called_only_on_root(self):
        resp = self.api_session_manager.post(
            f"{self.servizio.absolute_url()}/@message", json={}
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.post(
            f"{self.modello_pratica.absolute_url()}/@message", json={}
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.post(f"{self.portal_url}/@message", json={})
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 400)

    def test_add_record_can_called_only_by_authenticated_users(self):
        resp = self.api_session_anon.post(f"{self.portal_url}/@message", json={})
        self.assertEqual(resp.status_code, 401)

        resp = self.api_session_gestore.post(f"{self.portal_url}/@message", json={})
        self.assertEqual(resp.status_code, 400)

    def test_add_record_required_fields(self):
        # missing form_id
        resp = self.api_session_gestore.post(f"{self.portal_url}/@message", json={})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], 'Missing "message" field.')

        # also missing data
        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": "foo"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], 'Missing "message" field.')

        # now check that form_id is valid
        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": "foo", "message": "message"},
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], 'The value "foo" is not valid')

        # no records stored in the tool
        self.assertEqual(self.get_message_records()["items_total"], 0)

        pratica_id = self.api_session_gestore.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "data": "message"},
        ).json()["item_id"]

        # now is ok
        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={"pratica_id": pratica_id, "message": "message"},
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn("item_id", resp.json().keys())
        self.assertEqual(self.get_message_records()["items_total"], 2)

    def test_add_raise_error_if_state_not_pending(self):
        self.assertEqual(self.get_message_records()["items_total"], 0)
        pratica_id = self.api_session_gestore.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "data": "message"},
        ).json()["item_id"]
        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_id,
                "state": "foo",
                "message": "message",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            'Unable to create a record with "foo" initial state.',
        )

    def test_add_record_success(self):
        self.assertEqual(self.get_message_records()["items_total"], 0)
        pratica_id = self.api_session_gestore.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "data": "message"},
        ).json()["item_id"]

        resp = self.api_session_gestore.post(
            f"{self.portal_url}/@message",
            json={
                "pratica_id": pratica_id,
                "message": "message",
            },
        )
        self.assertEqual(resp.status_code, 200)

        records = self.get_message_records()
        self.assertEqual(records["items_total"], 2)
        self.assertEqual(records["items"][0]["message"], "message")
        self.assertEqual(records["items"][0]["state"], "pending")
        self.assertEqual(records["items"][0]["userid"], "gestore")

    # Deprecated
    # def test_not_gestore_cant_add(self):
    #     self.assertEqual(self.get_message_records()["items_total"], 0)
    #     pratica_id = self.api_session_auth.post(
    #         f"{self.portal_url}/@pratica",
    #         json={"form_id": self.modello_pratica.UID(), "data": "message"},
    #     ).json()["item_id"]

    #     resp = self.api_session_auth.post(
    #         f"{self.portal_url}/@message",
    #         json={
    #             "pratica_id": pratica_id,
    #             "message": "message",
    #         },
    #     )
    #     self.assertEqual(resp.status_code, 401)
