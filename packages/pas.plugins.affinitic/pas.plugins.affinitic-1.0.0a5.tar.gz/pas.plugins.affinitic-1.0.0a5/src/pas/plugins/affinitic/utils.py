# -*- coding: utf-8 -*-

from plone import api
from plone.memoize import ram
from time import time


@ram.cache(lambda *args: time() // (60 * 60))
def roles_list():
    """Return the current roles list"""
    return [
        r
        for r in api.portal.get_tool("portal_membership").getPortalRoles()
        if r not in ("Anonymous", "Owner", "Member")
    ]


@ram.cache(lambda *args: time() // (60 * 60))
def groups_list():
    """Return the existing groups"""
    return [
        g.id for g in api.group.get_groups()
        if g.id not in ("AuthenticatedUsers")
    ]