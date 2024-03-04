# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import re


with open("requirements.txt", "r", encoding="utf-8") as r:
    requirements = [i.strip() for i in r]

with open("aylak/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

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
    packages=[
        "aylak",
        "aylak.colors",
        "aylak.exceptions",
        "aylak.image",
        "aylak.rich",
        "aylak.telegram",
        "aylak.exceptions.colors",
    ],
    python_requires=">=3.10",
    requires=requirements,
    # ? PyPI Bilgileri
    long_description_content_type="text/markdown",
    # include_package_data=True,
)
