"""Command-line application for getting available Spark/Hadoop versions"""

from cleo.commands.command import Command
from cleo.helpers import option

from shui.functions import get_versions


class VersionsCommand(Command):
    """
    Get available Spark and Hadoop versions
    """

    name = "versions"
    description = "Get available Spark and Hadoop versions"
    options = [
        option(
            "latest", description="Show only the latest available version", flag=True
        )
    ]

    def handle(self):
        versions = get_versions()
        if self.option("latest"):
            versions = [sorted(versions)[-1]]
        for version in versions:
            self.line(f"Available version: {version}")
