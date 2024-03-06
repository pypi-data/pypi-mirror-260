# -*- coding: utf-8 -*-
from transaction import commit

from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiPatch(Mixin):
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

    def test_raises_unauthorized(self):
        resp = self.api_session_gestore.patch(
            f"{self.portal.absolute_url()}/@message/{self.message_id}",
            json={"message": "new one"},
        )

        self.assertEqual(resp.status_code, 401)
