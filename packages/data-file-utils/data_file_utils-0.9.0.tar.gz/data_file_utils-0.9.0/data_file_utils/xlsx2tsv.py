"""Convert Excel file to tab-delimited file."""
import click
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from pathlib import Path
from rich.console import Console
from typing import Optional


from file_utils import check_infile_status
from console_helper import print_green, print_yellow, print_red


DEFAULT_PROJECT = "data-file-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_HEADER_LINE = 1
DEFAULT_START_LINE = 2
DEFAULT_INCLUDE_LINE_NUMBERS = False

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


def excel_to_tsv(infile: str, outdir: str) -> None:
    """Convert the Excel file to a tab-delimited file.

    Args:
        infile (str): The Excel file to be converted.
        outdir (str): The output directory for the tab-delimited file.
    """
    # Read the Excel file
    logging.info(f"Will convert Excel file '{infile}'")
    excel_data = pd.read_excel(infile, sheet_name=None)

    # Iterate over each sheet
    for sheet_name, sheet_data in excel_data.items():
        logging.info(f"Will convert sheet '{sheet_name}'")

        # Generate the output file name
        outfile = os.path.join(outdir, f"{sheet_name.strip().replace(' ', '')}.tsv")

        # Write the sheet data to a tab-delimited file
        sheet_data.to_csv(outfile, sep='\t', index=False)

        print(f"Sheet '{sheet_name}' has been written to '{outfile}'")
        logging.info(f"Sheet '{sheet_name}' has been written to '{outfile}'")



def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
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
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: Optional[str], infile: str, logfile: Optional[str], outdir: Optional[str], verbose: Optional[bool]):
    """Convert Excel file to tab-delimited file.

    Args:
        config_file (Optional[str]): The configuration file for this project.
        infile (str): The Excel file to be converted into a tab-delimited file.
        logfile (Optional[str]): The log file.
        outdir (Optional[str]): The output directory.
        verbose (Optional[bool]): Will print more info to STDOUT.
    """
    error_ctr = 0

    if infile is None:
        print_red("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)


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

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    excel_to_tsv(infile, outdir)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
