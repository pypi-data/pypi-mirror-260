#!/usr/bin/env python3
import os
import pathlib
import shutil
import sys

from setuptools import Command
from setuptools import setup

NAME = "idem"
DESC = "Transform configuration into idempotent action."

with open("README.rst", encoding="utf-8") as f:
    LONG_DESC = f.read()

with open("requirements/base.txt") as f:
    REQUIREMENTS = f.read().splitlines()

REQUIREMENTS_EXTRA = {"full": set()}
EXTRA_PATH = pathlib.Path("requirements", "extra")
for extra in EXTRA_PATH.iterdir():
    with extra.open("r") as f:
        REQUIREMENTS_EXTRA[extra.stem] = f.read().splitlines()
        REQUIREMENTS_EXTRA["full"].update(REQUIREMENTS_EXTRA[extra.stem])

# Add extras for frozen dependencies
frozen_reqs = pathlib.Path("requirements")
for extra in EXTRA_PATH.iterdir():
    if extra.stem != "py3":
        continue

    frozen_deps = extra / "tests.txt"
    if not frozen_deps.exists():
        continue

    with frozen_deps.open("r") as f:
        # Omit lines that contain a #
        lines = [l for l in f.read().splitlines() if "#" not in l]
        minor_version = int(extra.suffix[1])
        REQUIREMENTS_EXTRA[f"frozen-3{extra.suffix}"] = lines
        # If the system python version matches the requirements, then add it as plain "frozen" extras
        if minor_version == sys.version_info[1]:
            REQUIREMENTS_EXTRA["frozen"] = lines


# Version info -- read without importing
_locals = {}
with open(f"{NAME}/version.py") as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals["version"]
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME, "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    # dot-delimited list of modules to not package. It's not good to package tests:
    skip_mods = ["tests"]
    for package in (NAME,):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, ".")
            if modname not in skip_mods:
                modules.append(modname)
    return modules


setup(
    name=NAME,
    author="VMware, Inc.",
    author_email="idemproject@vmware.com",
    url="https://docs.idemproject.io/idem/en/latest/index.html",
    project_urls={
        "Code": "https://gitlab.com/vmware/idem/idem",
        "Issue tracker": "https://gitlab.com/vmware/idem/idem/issues",
    },
    version=VERSION,
    description=DESC,
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRA,
    long_description=LONG_DESC,
    long_description_content_type="text/x-rst",
    license="Apache Software License 2.0",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        "console_scripts": [
            "idem = idem.scripts:start",
        ],
    },
    packages=discover_packages(),
    cmdclass={"clean": Clean},
)
