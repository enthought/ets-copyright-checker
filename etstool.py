# (C) Copyright 2018-2020 Enthought, Inc., Austin, TX
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

import subprocess
import sys

import click


# Directories and files that should be checked for flake8-cleanness.
FLAKE8_TARGETS = [
    "ets-copyright-checker",
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
    install_ets_copyright_checker = "edm run -e {environment} -- pip install "
    if editable:
        install_ets_copyright_checker += "--editable "
    install_ets_copyright_checker += "."

    commands = [
            "edm environments create {environment} --force --version={runtime}",
            "edm install -y -e {environment} flake8",
            install_ets_copyright_checker
        ]
    
    click.echo("Creating environment '{environment}'".format(**parameters))
    execute(commands, parameters)

    click.echo("Done install")


def test(runtime, environment):
    """ Run the test suite in a given environment.
    """
    parameters = get_parameters(runtime, environment)
    commands = [
        "edm run -e {environment} -- python -Xfaulthandler -m unittest "
        "discover -v ets-copyright-checker",
    ]
    click.echo("Running tests in '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done test")


def flake8(runtime, environment):
    """
    Run flake8 on all Python files.
    """
    parameters = get_parameters(runtime, environment)
    cmd = "edm run -e {environment} -- python -m flake8".format(**parameters) 
    cmd += " ".join(FLAKE8_TARGETS)

    if subprocess.call(cmd):
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
        "runtime": runtime,
        "environment": environment,
    }
    if environment is None:
        parameters["environment"] = "ets-copyright-checker-test-{runtime}".format(
            **parameters
        )
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


if __name__ == "__main__":
    cli()
