# -*- coding: utf-8 -*-

"""Top-level package for Vagon CLI"""

import click

from vagoncli import commands


__author__ = """Vagon, Inc."""
__email__ = 'info@vagon.io'
__version__ = '0.0.2'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)

def cli():
    """
    \b
    __     ___    ____  ___  _   _   ____ _____ ____  _____    _    __  __ ____
    \ \   / / \  / ___|/ _ \| \ | | / ___|_   _|  _ \| ____|  / \  |  \/  / ___|
     \ \ / / _ \| |  _| | | |  \| | \___ \ | | | |_) |  _|   / _ \ | |\/| \___ \\
      \ V / ___ \ |_| | |_| | |\  |  ___) || | |  _ <| |___ / ___ \| |  | |___) |
       \_/_/   \_\____|\___/|_| \_| |____/ |_| |_| \_\_____/_/   \_\_|  |_|____/

    Vagon CLI for managing Vagon Streams resources.

    \b
    Simple flow:
    - `vagon-cli configure` to save the Vagon Streams API Key and Secret
    - `vagon-cli application create [OPTIONS]` to create a new Application
    - `vagon-cli application version new [OPTIONS]` to deploy a new version to an existing Application
    - `vagon-cli performances` List available performance alternatives.
    - `vagon-cli deploy [OPTIONS]` to deploy a Vagon Stream Vendor Application [DEPRECATED]
    
    e.g. `vagon-cli application create --name my_app --zip-file app.zip --exec mouse.exe --performance 11`\n
    e.g. `vagon-cli application version new --zip-file app.zip --app-id 123 --exec app.exe --app-version v1.0-initial-build`

    Use --help on any command for more information."""
    pass


# Add commands
cli.add_command(commands.configure)


@click.group()
def application():
    """Manage applications, create a new one or upload a version."""
    pass

@click.group()
def version():
    """Manage application versions."""
    pass

version.add_command(commands.application_version, name="new") # new application version

application.add_command(commands.create_application, name="create") # create new application
application.add_command(version)

cli.add_command(application)
cli.add_command(commands.machine_types, name="performances") # machine-types
cli.add_command(commands.deploy, name="deploy") # application deploy
