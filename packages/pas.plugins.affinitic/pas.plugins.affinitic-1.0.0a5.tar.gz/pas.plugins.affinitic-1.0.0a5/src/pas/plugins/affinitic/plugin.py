# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import manage_users as ManageUsers
from AccessControl.class_init import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from operator import itemgetter
from pas.plugins.affinitic.interfaces import IAffiniticPlugin
from pas.plugins.authomatic.plugin import AuthomaticPlugin
from zope.interface import implementer

import logging
import os


logger = logging.getLogger(__name__)
template_directory = os.path.join(os.path.dirname(__file__), "browser")


def manage_addAffiniticPlugin(context, id="authomatic", title="", RESPONSE=None, **kw):
    """Create an instance of a Affinitic Plugin."""
    plugin = AffiniticPlugin(id, title, **kw)
    context._setObject(plugin.getId(), plugin)
    if RESPONSE is not None:
        RESPONSE.redirect("manage_workspace")

manage_addAffiniticPluginForm = PageTemplateFile("www/AffiniticPluginForm", globals())


@implementer(
    IAffiniticPlugin,
    pas_interfaces.IAuthenticationPlugin,
    pas_interfaces.IExtractionPlugin,
    pas_interfaces.IPropertiesPlugin,
    pas_interfaces.IUserEnumerationPlugin,
    pas_interfaces.IRolesPlugin,
    pas_interfaces.IGroupsPlugin,
    IUserIntrospection,
    IUserManagement,
    IDeleteCapability,
)
class AffiniticPlugin(AuthomaticPlugin):
    """Affinitic PAS Plugin"""

    security = ClassSecurityInfo()
    meta_type = "Affinitic Authentication Plugin"
    # BasePlugin.manage_options
    manage_options = (
        {"label": "Affinitic Users", "action": "manage_affiniticplugin"},
    ) + AuthomaticPlugin.manage_options
    security.declareProtected(ManagePortal, "manage_affiniticplugin")
    manage_affiniticplugin = PageTemplateFile(
        "zmi", globals(), __name__="manage_affiniticplugin"
    )

    # Tell PAS not to swallow our exceptions
    _dont_swallow_my_exceptions = True

    @security.protected(ManageUsers)
    def getPluginUsers(self):
        users = []
        for plugin_id, userid in self._userid_by_identityinfo:
            user = {}
            user["id"] = userid
            identity = self._useridentities_by_userid[userid]
            if hasattr(identity, "login"):
                user["login"] = identity.login
            else:
                user["login"] = ""
            user["email"] = identity.propertysheet.getProperty("email", "")
            user["fullname"] = identity.propertysheet.getProperty("fullname", "")
            user["plugin_type"] = plugin_id
            users.append(user)
        return users

    @security.private
    def getRolesForPrincipal(self, principal, request=None):
        """Fullfill RolesPlugin requirements"""
        identity = self._useridentities_by_userid.get(principal.getId(), None)
        if not identity:
            return ()
        if not identity._identities:
            return ()
        keys = [key for key in identity._identities.keys()]
        provider_id = keys[0]
        if "roles" in identity._identities[provider_id].keys():
            roles = identity._identities[provider_id]["roles"]
            if isinstance(roles, list):
                return tuple(roles)
            else:
                return ()
        else:
            return ()

    @security.private
    def getGroupsForPrincipal(self, principal, request=None):
        """Return the associated groups for the given principal"""
        identity = self._useridentities_by_userid.get(principal.getId(), None)
        if not identity:
            return ()
        if not identity._identities:
            return ()
        keys = [key for key in identity._identities.keys()]
        provider_id = keys[0]
        if "groups" in identity._identities[provider_id].keys():
            groups = identity._identities[provider_id]["groups"]
            if isinstance(groups, list):
                return tuple(groups)
            else:
                return ()
        else:
            return ()

    @security.private
    def extractCredentials(self, request):
        """Extract an OAuth2 bearer access token from the request.
        Implementation of IExtractionPlugin that extracts any 'Bearer' token
        from the HTTP 'Authorization' header.
        """
        # See RFC 6750 (2.1. Authorization Request Header Field) for details
        # on bearer token usage in OAuth2
        # https://tools.ietf.org/html/rfc6750#section-2.1

        creds = {}
        auth = request._auth
        if auth is None:
            return None
        if auth[:7].lower() == "bearer ":
            creds["token"] = auth.split()[-1]
        else:
            return None

        return creds


InitializeClass(AffiniticPlugin)
