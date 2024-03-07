"""Parse JSONL file and write multiple JSON files."""
import click
import json
import logging
import os
import pathlib
import sys

from datetime import datetime
from rich.console import Console
from typing import Optional

from console_helper import print_green, print_yellow, print_red
from file_utils import check_infile_status


DEFAULT_PROJECT = "data-file-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def parse_jsonl(input_file: str, output_folder: str) -> None:
    """Parse the JSONL file and write JSON files for each line.

    Args:
        input_file (str): The file path for the input JSONL file.
        output_folder (str): The output directory where the JSON files will be written to.
    """
    with open(input_file, 'r') as jsonl_file:
        for line_number, line in enumerate(jsonl_file, start=1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON at line {line_number}: {e}")
                continue

            output_file_path = os.path.join(output_folder, f"output_{line_number}.json")
            with open(output_file_path, 'w') as output_file:
                json.dump(data, output_file, indent=2)

            print(f"Processed line {line_number}. Output written to {output_file_path}")


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
@click.option('--infile', help="Required: The input JSONL file (.jsonl)")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help="Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(infile: str, logfile: Optional[str], outdir: Optional[str], verbose: Optional[bool]):
    """Parse JSONL file and write multiple JSON files."""
    error_ctr = 0

    if infile is None:
        print_red("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        print_red("Required command-line arguments were not provided")
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "jsonl")

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

    # Set the root logger
    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    parse_jsonl(infile, outdir)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
