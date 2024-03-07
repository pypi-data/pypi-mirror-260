import argparse
import pathlib
import os
import json
import re
import click

from ._cli_utils import ServiceParser, TestGenerator
from .__init__ import __version__, __library_name__
from ._config import Config

@click.group()
def cli():
    ...

@cli.command()
@click.argument("file", type=click.Path())
def eval(file):
    # This function as the CLI entrpy point for the cellmaps-sdk, which is used to verify and extract the schema from a dataprocessing service file.

    # Define Refex pattern for clear old cincodebio labels
    regex = re.compile(r'LABEL cincodebio\.schema=".*" \\ \n cincodebio\.ontology_version=".*"')

    # set the debug flag to True

    Config._DEBUG = True


    # parser = argparse.ArgumentParser(description="This is my program description")
    # parser.add_argument("filepath", help="This is the filepath to the file you want to verify and extract the schema from")

    # args = parser.parse_args()

    # Check if the filepath is absolute or relative
    if os.path.isabs(file):
        # check if file exists
        if not pathlib.Path(file).exists():
            raise FileNotFoundError(f"The file {file} does not exist")
    # case where path is relative
    else:
        # get the current working directory
        cwd = os.getcwd()
        # join the cwd with the relative path to get the absolute path
        absolute_path = os.path.join(cwd, file)
        # check if file exists
        if not pathlib.Path(absolute_path).exists():
            raise FileNotFoundError(f"The file {absolute_path} does not exist")
        
        # set the absolute path to the filepath
        file = absolute_path

    # Create a ServiceParser object
    service_parser = ServiceParser()
    dps_schema = (service_parser.get_schema(
        file_name=file
    ))

    
    # Read original dockerfile and remove old cincodebio labels
    with open(pathlib.Path(os.getcwd()) / "Dockerfile", 'r') as df:
        # Remove some content from the file
        fstr = re.sub(regex, '', df.read())

    # Overwrite the file with the version that has the cincodebio labels removed
    with open(pathlib.Path(os.getcwd()) / "Dockerfile", 'w') as df:
        df.write(fstr)

    # Add the new cincodebio labels
    with open(pathlib.Path(os.getcwd()) / "Dockerfile", 'a') as df:
        df.write(f'\nLABEL cincodebio.schema="{json.dumps(dps_schema)}" \ \n cincodebio.ontology_version="{__library_name__}~{__version__}"')

    
    tg = TestGenerator(dataclass_schemas=dps_schema)

    tg.generate_tests()

@cli.command()
def version():
    click.echo(f"{__library_name__} version {__version__}")

@cli.command()
def init():
    # Service Name 
    # Automated / Interactive
    # File Structure:
        # Dockerfile
            # Add some standard template too it
        # app/
        # requirements.txt
    ...


if __name__ == "__main__":
    cli()