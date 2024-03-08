# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory
from pas.plugins.affinitic.plugin import AffiniticPlugin
from pas.plugins.affinitic.plugin import manage_addAffiniticPlugin
from pas.plugins.affinitic.plugin import manage_addAffiniticPluginForm
from pas.plugins.affinitic.plugin import template_directory

import os


_ = MessageFactory("pas.plugins.affinitic")


def initialize(context):
    """Initializer called when used as a Zope 2 product"""
    registerMultiPlugin("Affinitic Authentication Plugin")
    context.registerClass(
        AffiniticPlugin,
        permission=add_user_folders,
        icon=os.path.join(template_directory, "static", "logo-authentication.svg"),
        constructors=(manage_addAffiniticPluginForm, manage_addAffiniticPlugin),
        visibility=None,
    )
