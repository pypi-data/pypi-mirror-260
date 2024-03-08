# -*- coding: utf-8 -*-

from authomatic import core
from authomatic.providers.oauth2 import OAuth2
from authomatic.providers.oauth2 import PROVIDER_ID_MAP
from plone.memoize import forever

import jwt
import requests


__all__ = ("OpenIDConnect",)


class OpenIDConnect(OAuth2):
    authorization_scope = [
        "email",
        "profile",
    ]
    user_info_scope = []
    provider_id = "oidc"

    supported_user_attributes = core.SupportedUserAttributes(
        id=True,
        name=True,
        username=True,
        first_name=True,
        last_name=True,
        email=True,
    )

    def __init__(self, *args, **kwargs):
        super(OpenIDConnect, self).__init__(*args, **kwargs)
        self.scope += self.authorization_scope

    @property
    def well_known_url(self):
        return self.settings.config[self.provider_id]["well_known"]

    @property
    @forever.memoize
    def well_known(self):
        resp = requests.get(self.well_known_url)
        return resp.json()

    @property
    def user_authorization_url(self):
        return self.well_known["authorization_endpoint"]

    @property
    def access_token_url(self):
        return self.well_known["token_endpoint"]

    @property
    def user_info_url(self):
        return self.well_known["userinfo_endpoint"]

    def _x_scope_parser(self, scope):
        """Parse scope and OpenID Connect have a space-separated scopes"""
        return " ".join(scope)

    @classmethod
    def _x_credentials_parser(cls, credentials, data):
        if data.get("token_type") == "bearer":
            credentials.token_type = cls.BEARER
        return credentials

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
            user.name = data.get("name")
            user.first_name = data.get("given_name")
            user.last_name = data.get("family_name")
            user.email = data.get("email")
            user.roles = ["Member"]
        return user


PROVIDER_ID_MAP.append(OpenIDConnect)
