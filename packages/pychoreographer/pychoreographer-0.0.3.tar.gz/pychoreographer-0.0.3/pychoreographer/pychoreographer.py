"""Console script for pychoreo."""
import sys
import subprocess
import json
import click


@click.group()
def cli():
    """A customizable Python library for automating file operations, system monitoring, and routine tasks"""  # noqa
    pass


@cli.command()
@click.option("--r", default="requirements.txt", help="requirements file")
def validate_deps(r):
    """Checks if the dependencies specified in a requirements file are installed in the current environment.

    Args:
        r (str): Path to the requirements.txt file. Defaults to "requirements.txt".

    Raises:
        FileNotFoundError: If the specified requirements file is not found.
    """  # noqa
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--format", "json"]
        ).decode("utf-8")
        installed_packages = {pkg["name"].lower(): pkg for pkg in json.loads(output)}  # noqa
        missing_depencies = []
        with open(r, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "==" not in line:
                    continue

                package_name, package_version = line.split("==")
                package_name = package_name.lower()
                if (
                    package_name not in installed_packages
                    or installed_packages[package_name]["version"] != package_version  # noqa
                ):
                    missing_depencies.append(f"{package_name}=={package_version}")  # noqa
        if len(missing_depencies) >= 1:
            click.echo("Missing Dependencies:")
            click.echo(missing_depencies)
        elif len(missing_depencies) == 0:
            click.echo("All dependencies are installed.")

    except FileNotFoundError:
        click.echo(f"Error: Requirements file '{r}' not found.")


if __name__ == "__main__":
    cli()
