# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from Products.CMFPlone.utils import get_installer
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from pas.plugins.affinitic import testing  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that pas.plugins.affinitic is properly installed."""

    layer = testing.PAS_PLUGINS_AFFINITIC_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if pas.plugins.affinitic is installed."""
        self.assertTrue(self.installer.is_product_installed("pas.plugins.affinitic"))

    def test_browserlayer(self):
        """Test that IPasPluginsAffiniticLayer is registered."""
        from pas.plugins.affinitic.interfaces import IPasPluginsAffiniticLayer
        from plone.browserlayer import utils

        self.assertIn(IPasPluginsAffiniticLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = testing.PAS_PLUGINS_AFFINITIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("pas.plugins.affinitic")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if pas.plugins.affinitic is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("pas.plugins.affinitic"))

    def test_browserlayer_removed(self):
        """Test that IPasPluginsAffiniticLayer is removed."""
        from pas.plugins.affinitic.interfaces import IPasPluginsAffiniticLayer
        from plone.browserlayer import utils

        self.assertNotIn(IPasPluginsAffiniticLayer, utils.registered_layers())
