# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from design.plone.iocittadino.testing import (  # noqa
    DESIGN_PLONE_IOCITTADINO_INTEGRATION_TESTING,
)


class GroupTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOCITTADINO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_group_created_on_install(self):
        self.assertNotEqual(api.group.get(groupname="operatori_pratiche"), None)
