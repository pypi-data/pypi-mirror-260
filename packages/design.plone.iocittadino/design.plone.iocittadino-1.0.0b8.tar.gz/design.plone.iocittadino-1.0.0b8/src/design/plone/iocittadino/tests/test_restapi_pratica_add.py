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
            f"{self.servizio.absolute_url()}/@pratica", json={}
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.post(
            f"{self.modello_pratica.absolute_url()}/@pratica", json={}
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.post(f"{self.portal_url}/@pratica", json={})
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 400)

    def test_add_record_can_called_only_by_authenticated_users(self):
        resp = self.api_session_anon.post(f"{self.portal_url}/@pratica", json={})
        self.assertEqual(resp.status_code, 401)

        resp = self.api_session_auth.post(f"{self.portal_url}/@pratica", json={})
        self.assertEqual(resp.status_code, 400)

    def test_add_record_required_fields(self):
        # missing form_id
        resp = self.api_session_auth.post(f"{self.portal_url}/@pratica", json={})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], 'Missing "form_id" field.')

        # also missing data
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica", json={"form_id": "foo"}
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], "Missing form data.")

        # now check that form_id is valid
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": "foo", "data": "bar"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["message"], 'Wrong form_id "foo". Item not found.')

        # no records stored in the tool
        self.assertEqual(self.get_pratica_records()["items_total"], 0)

        # now is ok
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "data": "bar"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("item_id", resp.json().keys())
        self.assertEqual(self.get_pratica_records()["items_total"], 1)

    def test_add_raise_error_if_state_not_draft(self):
        self.assertEqual(self.get_pratica_records()["items_total"], 0)
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "state": "foo"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            'Unable to create a record with "foo" initial state.',
        )

    def test_add_record_data_not_required_if_state_draft(self):
        self.assertEqual(self.get_pratica_records()["items_total"], 0)
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={"form_id": self.modello_pratica.UID(), "state": "draft"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("item_id", resp.json().keys())
        self.assertEqual(self.get_pratica_records()["items_total"], 1)

    def test_add_record_success(self):
        self.assertEqual(self.get_pratica_records()["items_total"], 0)
        resp = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "foo",
            },
        )
        self.assertEqual(resp.status_code, 200)

        records = self.get_pratica_records()
        self.assertEqual(records["items_total"], 1)
        self.assertEqual(records["items"][0]["state"], "ongoing")
        self.assertEqual(records["items"][0]["userid"], "foo")
