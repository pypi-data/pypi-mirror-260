"""Convert the tab-delimited file to a JSON file."""
import click
import csv
import json
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from pathlib import Path
from rich.console import Console
from typing import Any, Dict, Optional

from .file_utils import check_infile_status
from .console_helper import print_green, print_red, print_yellow


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


def convert_file(
    infile: str,
    outfile: str,
    header_line: int = DEFAULT_HEADER_LINE,
    start_line: int = DEFAULT_START_LINE,
    include_line_numbers: bool = DEFAULT_INCLUDE_LINE_NUMBERS
) -> None:
    """Convert the tab-delimited file to a JSON file.

    Args:
        infile (str): The tab-delimited file to be converted.
        outfile (str): The output JSON file.
        header_line (int, optional): The line number that contains the column headers. Defaults to DEFAULT_HEADER_LINE.
        start_line (int, optional): The line number where the first record begins. Defaults to DEFAULT_START_LINE.
        include_line_numbers (bool, optional): If True, the output will include the line number of the record in the source tab-delimited file. Defaults to DEFAULT_INCLUDE_LINE_NUMBERS.
    """

    record_lookup = get_record_lookup(infile, header_line, start_line, include_line_numbers)
    # Write the list of ordered dictionaries to a JSON file
    lookup = {
        "infile": os.path.abspath(infile),
        "records": record_lookup
    }
    with open(outfile, 'w', encoding='utf-8') as json_file:
        json.dump(lookup, json_file, indent=2)

def get_record_lookup(infile: str, header_line: int = 2, start_line: int = 3, include_line_numbers: bool = DEFAULT_INCLUDE_LINE_NUMBERS) -> Dict[str, Any]:
    """Parse the input tab-delimited file and get the record lookup.

    Args:
        infile (str): The input tab-delimited file.
        header_line (int, optional): The line number at which the column headers can be found. Defaults to 2.
        start_line (int, optional): The line number at which the first record can be found. Defaults to 3.
        include_line_numbers (bool, optional): If True, the line numbers will be included in the record objects in the JSON file. Defaults to DEFAULT_INCLUDE_LINE_NUMBERS.

    Raises:
        Exception: If the input file does not exist.

    Returns:
        Dict[str, Any]: The record lookup.
    """

    if not os.path.exists(infile):
        raise Exception(f"file '{infile}' does not exist")

    header_to_position_lookup = {}
    position_to_header_lookup = {}
    # record_list = []
    master_record_lookup = {}
    record_ctr = 0

    with open(infile) as f:
        reader = csv.reader(f, delimiter='\t')
        for line_num, row in enumerate(reader):
            if line_num < header_line:
                logging.info(f"Will ignore line '{line_num}': {row}")
                continue
            if line_num == header_line:
                for field_ctr, field in enumerate(row):
                    header_to_position_lookup[field] = field_ctr
                    position_to_header_lookup[field_ctr] = field
                logging.info(f"Processed the header of tab-delimited file '{infile}'")
            elif line_num > header_line:
                record_lookup = {}

                if include_line_numbers:
                    record_lookup["line_num"] = line_num

                for field_ctr, value in enumerate(row):
                    field_name = position_to_header_lookup[field_ctr]
                    record_lookup[field_name] = value
                # record_list.append(record_lookup)
                master_record_lookup[line_num] = record_lookup
                record_ctr += 1
        logging.info(f"Processed '{record_ctr}' records in csv file '{infile}'")

    return master_record_lookup


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
@click.option('--header_line', help=f"Optional: The line number the header row begins - default is '{DEFAULT_HEADER_LINE}'")
@click.option('--include_line_numbers', is_flag=True, help=f"Optional: To include the line numbers in the JSON - default is '{DEFAULT_INCLUDE_LINE_NUMBERS}'")
@click.option('--infile', help="Required: The primary input file")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output final report file")
@click.option('--start_line', help=f"Optional: The line number the data rows begin - default is '{DEFAULT_START_LINE}'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: Optional[str], header_line: Optional[int], include_line_numbers: Optional[bool], infile: str, logfile: Optional[str], outdir: Optional[str], outfile: Optional[str], start_line: Optional[int], verbose: Optional[bool]):
    """Convert tab-delimited file into JSON file."""

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

    if header_line is None:
        header_line = DEFAULT_HEADER_LINE
        print_yellow(f"--header_line was not specified and therefore was set to '{header_line}'")

    if include_line_numbers is None:
        include_line_numbers = DEFAULT_INCLUDE_LINE_NUMBERS
        print_yellow(f"--include_line_numbers was not specified and therefore was set to '{include_line_numbers}'")

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
            os.path.splitext(os.path.basename(__file__))[0] + '.json'
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    if start_line is None:
        start_line = DEFAULT_START_LINE
        print_yellow(f"--start_line was not specified and therefore was set to '{start_line}'")

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
        start_line=start_line,
        header_line=header_line,
        include_line_numbers=include_line_numbers
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
