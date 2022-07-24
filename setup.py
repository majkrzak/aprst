#!/usr/bin/env python

from distutils.core import setup

setup(
    name="aprst",
    description="APRS-IS feed polyfill creating status packet out of self to self message.",
    author="Piotr Majkrzak",
    author_email="piotr@majkrzak.dev",
    packages=["aprst"],
    package_dir={"aprst": "./src"},
    install_requires=["aprslib"],
)
