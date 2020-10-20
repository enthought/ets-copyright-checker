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


if __name__ == "__main__":
    setuptools.setup(
        name="ets_copyright_checker",
        version="1.0.0",
        description="flake8 plugin for checking copyright headers",
        install_requires=["flake8"],
        packages=["ets_copyright_checker", "ets_copyright_checker.tests"],
        entry_points={
            "flake8.extension": [
                "H = ets_copyright_checker:CopyrightHeaderExtension",
            ],
        },
    )
