# -*- coding: utf-8 -*-
"""Installer for the pas.plugins.affinitic package."""

from setuptools import find_packages
from setuptools import setup

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="pas.plugins.affinitic",
    version="1.0.0a5",
    description="Collection of authentication tools and plugins",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Affinitic",
    author_email="support@affinitic.be",
    url="https://github.com/affinitic/pas.plugins.affinitic",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/pas.plugins.affinitic",
        "Source": "https://github.com/affinitic/pas.plugins.affinitic",
        "Tracker": "https://github.com/affinitic/pas.plugins.affinitic/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["pas"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pas.plugins.authomatic",
        "plone.api",
        "plone.restapi",
        "requests",
        "setuptools",
        "z3c.jbot",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes",
            "plone.app.iterate",
            "plone.app.robotframework[debug]",
            "plone.app.testing",
            "plone.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = pas.plugins.affinitic.locales.update:update_locale
    """,
)
