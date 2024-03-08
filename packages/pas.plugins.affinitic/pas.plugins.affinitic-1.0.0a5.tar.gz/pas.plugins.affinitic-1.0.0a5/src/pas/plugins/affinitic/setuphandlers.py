# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from pas.plugins.affinitic.plugin import AffiniticPlugin
from plone import api
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "pas.plugins.affinitic:uninstall",
        ]


def _add_plugin(pas, pluginid="authomatic"):
    if pluginid in pas.objectIds():
        if isinstance(pas[pluginid], AffiniticPlugin):
            return pluginid + " already installed."
        else:
            pas._delObject(pluginid)
    plugin = AffiniticPlugin(pluginid, title="Affinitic Auth Plugin")
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info["interface"]
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface, [x[0] for x in pas.plugins.listPlugins(interface)[:-1]]
        )


def post_install(context):
    """Post install script"""
    _add_plugin(api.portal.get_tool("acl_users"))
    api.portal.set_registry_record(
        "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings.userid_factory_name",
        "userid",
    )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
