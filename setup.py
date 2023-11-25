# -*- coding: utf-8 -*-
"""

"""

from __future__ import absolute_import

from os.path import dirname, join
from setuptools import setup, find_namespace_packages, find_packages

__copyright__ = "Copyright (c) 2015-2019 Ing. Petr Jindra. All Rights Reserved."


SRC_DIR = "src"

requirements_base_path = join(dirname(__file__))


def get_requirements(filename):
    requirements_path = join(requirements_base_path, filename)
    with open(requirements_path, "r") as fd:
        return [r for r in fd]


def get_version():
    version_dict = dict()
    exec(open("src/crudalchemy/version.py").read(), version_dict)
    return version_dict["__version__"]


def main():
    setup(
        version=get_version(),
        name="crud-alchemy",
        package_dir={"": SRC_DIR},
        install_requires=get_requirements("requirements.txt"),
        data_files=[("", ["requirements.txt", "requirements.dev.txt", "requirements.gbol.txt"])],
        extras_require={
            "dev": get_requirements("requirements.dev.txt"),
            "gbol": get_requirements("requirements.gbol.txt"),
        }
    )


if __name__ == "__main__":
    main()
