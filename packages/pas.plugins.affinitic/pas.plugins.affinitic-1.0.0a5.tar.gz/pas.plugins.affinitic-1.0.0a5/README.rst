=====================
pas.plugins.affinitic
=====================

Collection of authentication tools and plugins

Features
--------

- Authomatic provider for Keycloak


Configuration Example
---------------------

example for keycloak::

    {
        "keycloak": {
            "id": 1,
            "display": {
                "title": "Keycloak",
                "cssclasses": {
                    "button": "plone-btn plone-btn-default",
                    "icon": "glypicon glyphicon-github"
                },
                "as_form": false
            },
            "propertymap": {
                "email": "email",
                "name": "fullname"
            },
            "well_known": "http://localhost:9080/realms/Test/.well-known/openid-configuration",
            "class_": "pas.plugins.affinitic.providers.keycloak.Keycloak",
            "consumer_key": "Client Name",
            "consumer_secret": "secret key",
            "access_headers": {
                "User-Agent": "Plone (pas.plugins.authomatic)"
            }
        }
    }

example for openidconnect::

    {
        "oidc": {
            "id": 1,
            "display": {
                "title": "OIDC",
                "cssclasses": {
                    "button": "plone-btn plone-btn-default",
                    "icon": "glypicon glyphicon-github"
                },
                "as_form": false
            },
            "propertymap": {
                "email": "email",
                "name": "fullname"
            },
            "well_known": "http://localhost:9080/realms/Test/.well-known/openid-configuration",
            "class_": "pas.plugins.affinitic.providers.openidconnect.OpenIDConnect",
            "consumer_key": "Client Name",
            "consumer_secret": "secret key",
            "access_headers": {
                "User-Agent": "Plone (pas.plugins.authomatic)"
            }
        }
    }


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at ...


Translations
------------

This product has been translated into

- French


Installation
------------

Install pas.plugins.affinitic by adding it to your buildout::

    [buildout]

    ...

    eggs =
        pas.plugins.affinitic


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/affinitic/pas.plugins.affinitic/issues
- Source Code: https://github.com/affinitic/pas.plugins.affinitic


Support
-------

If you are having issues, please let us know.


License
-------
The project is licensed under the GPLv2.
