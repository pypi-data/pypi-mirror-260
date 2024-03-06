# -*- coding: utf-8 -*-
import base64
from urllib.error import HTTPError

import transaction
from pkg_resources import resource_string
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser

from design.plone.iocittadino.tests.restapi_mixin import Mixin

PDF_B64 = base64.b64encode(
    resource_string("design.plone.iocittadino.tests", "dummy.pdf")
)


class TestRestapiGet(Mixin):
    def setUp(self):
        super().setUp()
        self.browser = Browser(self.layer["app"])
        self.pratica_id = self.pratica_storage.add(
            {
                "form_id": self.modello_pratica.UID(),
                "data": "a value",
            }
        ).intid

        self.message_initial_state = "pending"
        self.message_text = "Testing message"
        self.message_id = self.message_storage.add(
            {
                "pratica_id": self.pratica_id,
                "message": self.message_text,
                "attachments": [
                    {
                        "name": "dummy.txt",
                        "data": "data:plain/text;base64,ZHVtbXkgdGV4dCBmaWxl",
                    },
                    {
                        "name": "dummy.pdf",
                        "data": f"data:application/pdf;base64,${PDF_B64}",
                    },
                ],
            }
        ).intid

        transaction.commit()

    def test_get_need_to_be_called_on_root(self):
        resp = self.api_session_manager.get(
            f"{self.servizio.absolute_url()}/@message",
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.api_session_manager.get(
            f"{self.modello_pratica.absolute_url()}/@message",
        )
        # because we're passing wrong data
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@message",
        )

        self.assertEqual(resp.status_code, 400)

    def test_get_need_id_as_parameter(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@message",
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_return_not_found_for_wrong_id(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@message/foo",
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_return_serialized_data(self):
        resp = self.api_session_manager.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        self.assertEqual(res["item_id"], self.message_id)
        self.assertEqual(res["pratica"]["item_id"], self.pratica_id)
        self.assertEqual(res["userid"], api.user.get_current().getId())
        self.assertEqual(res["state"], self.message_initial_state)
        self.assertEqual(res["message"], self.message_text)

        # TODO: use freezegun to fixture the datetime.now
        self.assertIn("date", res.keys())

    def test_anon_cant_get_data(self):
        resp = self.api_session_anon.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 401)

    def test_users_cant_get_record_from_other_users(self):
        resp = self.api_session_auth.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 401)

    def test_gestori_can_get_record(self):
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        self.assertEqual(res["pratica"]["item_id"], self.pratica_id)
        self.assertEqual(res["userid"], api.user.get_current().getId())
        self.assertEqual(res["state"], self.message_initial_state)
        self.assertEqual(res["message"], self.message_text)
        self.assertIn("date", res.keys())

    def test_message_attachments(self):
        resp = self.api_session_gestore.get(
            f"{self.portal_url}/@message/{self.message_id}",
        )
        self.assertEqual(resp.status_code, 200)

        res = resp.json()
        attachments = res["attachments"]
        self.assertEqual(
            ["dummy.txt", "dummy.pdf"],
            [a["name"] for a in attachments],
        )

        # TODO: usare attachments[0]["url"]
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        self.browser.open(
            f"{self.portal_url}/++api++/@message/{self.message_id}/@@download/0/file1.txt",
        )
        self.assertEqual(self.browser._response.status, "200 OK")
        self.assertEqual(
            self.browser._response.content_disposition,
            'attachment; filename="dummy.txt"',
        )
        self.assertEqual(self.browser.contents, b"dummy text file")

        self.browser.open(
            f"{self.portal_url}/++api++/@message/{self.message_id}/@@download/1/file2.pdf",
        )
        self.assertEqual(self.browser._response.status, "200 OK")
        self.assertEqual(
            self.browser._response.content_disposition,
            'attachment; filename="dummy.pdf"',
        )
        # self.assertEqual(self.browser.contents, resource_string("design.plone.iocittadino.tests", "dummy.pdf"))

        # 404
        self.assertRaises(
            HTTPError,
            self.browser.open,
            f"{self.portal_url}/++api++/@message/{self.message_id}/@@download/2/file3.pdf",
        )
