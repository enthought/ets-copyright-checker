# (C) Copyright 2020-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Tasks for Test Runs
===================

This file is intended to be used with a python environment with the
click library to automate the process of setting up test environments
and running the test within them.  This improves repeatability and
reliability of tests be removing many of the variables around the
developer's particular Python environment.  Test environment setup and
package management is performed using `EDM
http://docs.enthought.com/edm/`_

To use this to run you tests, you will need to install EDM and click
into your working environment.  You will also need to have git
installed to access required source code from github repositories.
You can then do::

    python etstool.py install --runtime=...

to create a test environment from the current codebase and::

    python etstool.py test --runtime=...

to run tests in that environment.

If you need to make frequent changes to the source, it is often convenient
to install the source in editable mode::

    python etstool.py install --editable --runtime=...

Tests can still be run via the usual means in other environments if that suits
a developer's purpose.
"""

import os
import shutil
import subprocess
import sys

import click


# Directories and files that should be checked for flake8-cleanness.
FLAKE8_TARGETS = [
    "flake8_ets",
    "etstool.py",
    "setup.py",
]


# All commands are implemented as subcommands of the cli group.
@click.group()
def cli():
    pass


@cli.command()
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--environment", default=None, help="EDM environment to use")
@click.option(
    "--editable/--not-editable",
    default=False,
    help="Install main package in 'editable' mode?  [default: --not-editable]",
)
def install(runtime, environment, editable):
    """ Install project and dependencies into a clean EDM environment.=
    """
    parameters = get_parameters(runtime, environment)
    # Install local source
    install_flake8_ets = "{edm} run -e {environment} -- pip install "
    if editable:
        install_flake8_ets += "--editable "
    install_flake8_ets += "."

    commands = [
            "{edm} environments create {environment}"
            " --force --version={runtime}",
            "{edm} install -y -e {environment} flake8",
            install_flake8_ets
        ]

    click.echo("Creating environment '{environment}'".format(**parameters))
    execute(commands, parameters)

    click.echo("Done install")


@cli.command()
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--environment", default=None, help="EDM environment to use")
def test(runtime, environment):
    """ Run the test suite in a given environment.
    """
    parameters = get_parameters(runtime, environment)
    commands = [
        "{edm} run -e {environment} -- python -Xfaulthandler -m unittest "
        "discover -v flake8_ets",
    ]
    click.echo("Running tests in '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done test")


@cli.command()
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--environment", default=None, help="EDM environment to use")
def flake8(runtime, environment):
    """
    Run flake8 on all Python files.
    """
    parameters = get_parameters(runtime, environment)
    cmd = "{edm} run -e {environment} -- python -m flake8 ".format(
        **parameters)
    cmd += " ".join(FLAKE8_TARGETS)

    if subprocess.call(cmd.split()):
        click.echo()
        raise click.ClickException("Flake8 check failed.")
    else:
        click.echo("Flake8 check succeeded.")


# ----------------------------------------------------------------------------
# Utility routines
# ----------------------------------------------------------------------------

def get_parameters(runtime, environment):
    """ Set up parameters dictionary for format() substitution """

    parameters = {
        "edm": locate_edm(),
        "runtime": runtime,
        "environment": environment,
    }
    if environment is None:
        parameters["environment"] = \
            "flake8-ets-test-{runtime}".format(**parameters)
    return parameters


def execute(commands, parameters):
    for command in commands:
        click.echo("[EXECUTING] {}".format(command.format(**parameters)))
        try:
            subprocess.check_call(
                [arg.format(**parameters) for arg in command.split()]
            )
        except subprocess.CalledProcessError as exc:
            print(exc)
            sys.exit(1)


def locate_edm():
    """
    Locate an EDM executable if it exists, else raise an exception.

    Returns the first EDM executable found on the path. On Windows, if that
    executable turns out to be the "edm.bat" batch file, replaces it with the
    executable that it wraps: the batch file adds another level of command-line
    mangling that interferes with things like specifying version restrictions.

    Returns
    -------
    edm : str
        Path to the EDM executable to use.

    Raises
    ------
    click.ClickException
        If no EDM executable is found in the path.
    """
    edm = shutil.which("edm")
    if edm is None:
        raise click.ClickException(
            "This script requires EDM, but no EDM executable "
            "was found on the path."
        )

    # Resolve edm.bat on Windows.
    if sys.platform == "win32" and os.path.basename(edm).lower() == "edm.bat":
        edm = os.path.join(os.path.dirname(edm), "embedded", "edm.exe")

    return edm


if __name__ == "__main__":
    cli()
