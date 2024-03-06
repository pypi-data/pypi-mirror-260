# -*- coding: utf-8 -*-
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiPatch(Mixin):
    def setUp(self):
        super().setUp()
        self.pratica_id = self.api_session_auth.post(
            f"{self.portal_url}/@pratica",
            json={
                "form_id": self.modello_pratica.UID(),
                "data": "foo",
                "state": "draft",
            },
        ).json()["item_id"]

    def test_update_record_can_called_only_on_root(self):
        resp = self.api_session_manager.patch(
            f"{self.servizio.absolute_url()}/@pratica/{self.pratica_id}",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.patch(
            f"{self.modello_pratica.absolute_url()}/@pratica/{self.pratica_id}",
            json={},
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json={},
        )
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 400)

    def test_update_return_404_if_pratica_id_not_passed(self):
        resp = self.api_session_manager.patch(f"{self.portal_url}/@pratica", json={})
        # because we're passing wrong data
        self.assertEqual(resp.status_code, 404)

    def test_update_record_required_data(self):
        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}", json={}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "Missing required field: data or assigned_to.",
        )

        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json={"data": {}},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "Missing required field: data or assigned_to.",
        )

        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json={"data": "bar"},
        )
        self.assertEqual(resp.status_code, 200)

    def test_passing_wrong_pratica_id_type_return_400(self):
        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/xxx", json={"data": "bar"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_passing_wrong_pratica_id_return_404(self):
        resp = self.api_session_manager.patch(
            f"{self.portal_url}/@pratica/0000", json={"data": "bar"}
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_record_can_called_only_by_same_user_or_who_have_right_permissions(
        self,
    ):
        data = {"data": "bar"}

        record = self.api_session_manager.get(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
        ).json()
        self.assertEqual(record["data"], "foo")

        resp = self.api_session_anon.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json=data,
        )
        self.assertEqual(resp.status_code, 401)

        # an user different by the creator, can't access the record
        resp = self.api_session_other.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json=data,
        )
        self.assertEqual(resp.status_code, 401)

        resp = self.api_session_auth.patch(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
            json=data,
        )

        self.assertEqual(resp.status_code, 200)
        record = self.api_session_manager.get(
            f"{self.portal_url}/@pratica/{self.pratica_id}",
        ).json()

        self.assertEqual(record["data"], "bar")
