# (C) Copyright 2018-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import setuptools


def get_long_description():
    """ Read long description from README.rst. """
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read()


if __name__ == "__main__":
    setuptools.setup(
        name="flake8-ets",
        version="1.0.0",
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
        packages=["ets_copyright_checker", "ets_copyright_checker.tests"],
        entry_points={
            "flake8.extension": [
                "H = ets_copyright_checker:CopyrightHeaderExtension",
            ],
        },
    )
