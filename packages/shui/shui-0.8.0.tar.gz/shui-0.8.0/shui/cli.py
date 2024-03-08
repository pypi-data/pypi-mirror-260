"""Command line entrypoint for shui application"""

from cleo.application import Application

from shui import __version__
from shui.commands import InstallCommand, VersionsCommand

application = Application("shui", __version__)
application.add(InstallCommand())
application.add(VersionsCommand())


def main():
    """Command line entrypoint for shui application"""
    application.run()
