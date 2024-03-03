# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aylak import __version__ as version

setup(
    # ? Genel Bilgiler
    name="aylak",
    version=version,
    url="https://github.com/aylak-github/aylak-pypi",
    description="Aylak PyPi",
    keywords=["aylak", "pypi", "aylak-pypi", "aylak-pypi"],
    author="aylak-github",
    author_email="contact@yakupkaya.net.tr",
    license="GNU AFFERO GENERAL PUBLIC LICENSE (v3)",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    # ? Paket Bilgileri
    packages=["aylak"],
    python_requires=">=3.10",
    # install_requires=["pythonansi", "aiofiles", "cryptography"],
    requires=["pythonansi", "aiofiles", "cryptography"],
    # ? PyPI Bilgileri
    long_description_content_type="text/markdown",
    include_package_data=True,
)
