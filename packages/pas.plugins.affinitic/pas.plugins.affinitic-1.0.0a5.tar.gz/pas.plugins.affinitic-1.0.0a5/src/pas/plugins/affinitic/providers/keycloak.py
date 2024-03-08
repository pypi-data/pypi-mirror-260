# -*- coding: utf-8 -*-

from authomatic.providers.oauth2 import PROVIDER_ID_MAP
from pas.plugins.affinitic import utils
from pas.plugins.affinitic.providers.openidconnect import OpenIDConnect

import jwt


__all__ = ("Keycloak",)


class Keycloak(OpenIDConnect):
    provider_id = "keycloak"

    @staticmethod
    def _x_user_parser(user, data):
        encoded = data.get("access_token")
        if encoded:
            payload_data = jwt.decode(
                encoded,
                algorithms=["RS256"],
                options={"verify_signature": False, "verify_aud": False},
            )
            user.id = payload_data["sub"]
            data = payload_data
        if "sub" in data.keys():
            user.username = data.get("preferred_username")
            user.name = data.get("name")
            user.first_name = data.get("given_name")
            user.last_name = data.get("family_name")
            user.email = data.get("email")
            user.roles = ["Member"]
            roles = data.get("realm_access", {}).get('roles', [])
            user.roles.extend([r for r in roles if r in utils.roles_list()])
            user.groups = []
            groups = [g.replace("/", "") for g in data.get("groups", [])]
            user.groups.extend([g for g in groups if g in utils.groups_list()])
        return user


PROVIDER_ID_MAP.append(Keycloak)
