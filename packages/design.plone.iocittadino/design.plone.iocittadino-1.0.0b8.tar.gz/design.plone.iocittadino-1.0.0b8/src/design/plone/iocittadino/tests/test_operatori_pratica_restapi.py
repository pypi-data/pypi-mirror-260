# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.restapi.testing import RelativeSession

from design.plone.iocittadino.testing import (
    DESIGN_PLONE_IOCITTADINO_API_FUNCTIONAL_TESTING,
)


class TestGroupRestapi(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        api.user.create(
            email="jdoe@example.com",
            username="jdoe",
            properties=dict(fullname="John Doe"),
            password="secret123",
        )
        api.group.add_user(groupname="operatori_pratiche", username="jdoe")

        transaction.commit()

    def test_return_operatori_list(self):
        resp = self.api_session.get(
            f"{self.portal_url}/@operatori_pratica",
        ).json()

        self.assertEqual(resp["items"], [{"value": "jdoe", "label": "John Doe"}])
