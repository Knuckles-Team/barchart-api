#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from barchart_api.version import __version__, __author__
from pathlib import Path
import os
import re
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements


readme = Path("README.md").read_text()
version = __version__
requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), session=PipSession()
)
readme = re.sub(r"Version: [0-9]*\.[0-9]*\.[0-9][0-9]*", f"Version: {version}", readme)
with open("README.md", "w") as readme_file:
    readme_file.write(readme)
description = "Unofficial API for https://www.barchart.com/"

setup(
    name="barchart-api",
    version=f"{version}",
    description=description,
    long_description=f"{readme}",
    long_description_content_type="text/markdown",
    url="https://github.com/Knuckles-Team/barchart-api",
    author=__author__,
    author_email="knucklessg1@gmail.com",
    license="MIT",
    packages=["barchart_api"],
    include_package_data=True,
    install_requires=[str(requirement.requirement) for requirement in requirements],
    py_modules=["barchart_api"],
    package_data={"barchart_api": ["barchart_api"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Public Domain",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
