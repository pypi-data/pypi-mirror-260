"""Convert a comma-separated file into a tab-delimited file."""
import click
import csv
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from pathlib import Path
from rich.console import Console
from typing import Optional

from .file_utils import check_infile_status
from .console_helper import print_green, print_red, print_yellow


DEFAULT_PROJECT = "data-file-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.yaml'
)


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def convert_file(
    infile: str,
    outfile: str,
) -> None:
    """Convert the comma-separated file into a tab-delimited file.

    Args:
        infile (str): The tab-delimited file to be converted.
        outfile (str): The output JSON file.
    """

    # Open the CSV file
    with open(infile, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Open the TSV file
        with open(outfile, 'w') as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter='\t')

            # Write each row from the CSV file to the TSV file
            for row in csv_reader:
                tsv_writer.writerow(row)

    print(f"Wrote tab-delimited file '{outfile}'")

def validate_verbose(ctx, param, value):
    """Validate the verbose flag.

    Args:
        ctx (Context): The click context.
        param (str): The parameter name.
        value (bool): The value of the parameter.

    Returns:
        bool: The value of the parameter.
    """
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"Optional: The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--infile', help="Required: The primary input file")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output final report file")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(
    config_file: Optional[str],
    infile: str,
    logfile: Optional[str],
    outdir: Optional[str],
    outfile: Optional[str],
    verbose: Optional[bool]
):
    """Convert a comma-separated file into a tab-delimited file."""

    error_ctr = 0

    if infile is None:
        print_red("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "csv")

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")


    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.tsv'
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    convert_file(
        infile,
        outfile,
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
