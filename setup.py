# (C) Copyright 2020-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import runpy
import setuptools


def get_version():
    """ Extract version string from version.py. """
    version_filename = os.path.join("flake8_ets", "version.py")
    info = runpy.run_path(version_filename)
    return info["version"]


def get_long_description():
    """ Read long description from README.rst. """
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read()


if __name__ == "__main__":
    setuptools.setup(
        name="flake8-ets",
        version=get_version(),
        author="Enthought",
        author_email="info@enthought.com",
        url="https://github.com/enthought/ets-copyright-checker",
        description=(
            "flake8 plugin for checking Enthought Tool Suite copyright "
            "headers."
        ),
        long_description=get_long_description(),
        long_description_content_type="text/x-rst",
        install_requires=["flake8"],
        packages=setuptools.find_packages(
            include=[
                "flake8_ets",
                "flake8_ets.*",
            ],
        ),
        entry_points={
            "flake8.extension": [
                "H = flake8_ets.copyright_header:CopyrightHeaderExtension",
            ],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
        ],
        python_requires=">=3.5",
        license="BSD",
    )
