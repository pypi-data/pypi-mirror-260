"""Find the last directory in the specified directory given a directory pattern."""
import click
import logging
import os
import pathlib
import re
import sys
import yaml

from pathlib import Path
from datetime import datetime
from rich.console import Console
from typing import Optional

from .file_utils import calculate_md5, get_file_creation_date, get_file_list, get_file_size, get_line_count, check_infile_status
from .console_helper import print_green, print_yellow


DEFAULT_PROJECT = "data-file-utils"

DEFAULT_ISDIR = False

DEFAULT_NO_DETAILS = False

DEFAULT_OUTDIR = os.path.join(
    '/tmp',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
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

def profile_directory(indir: str, no_details: bool = False) -> None:
    """Profile the files in the specified directory.

    Args:
        indir (str): The input directory to check for assets.
        no_details (bool, optional): If True, print more details to STDOUT. Defaults to False.
    """
    file_list = get_file_list(indir)

    console.print(f"Found the following '{len(file_list)}' files:")

    for f in file_list:
        profile_file(f, no_details)
        # if not no_details:
        #     print("\n")

def profile_file(infile: str, no_details: bool = False) -> None:
    """Profile the specified file.

    Args:
        infile (str): The input file to profile.
        no_details (bool, optional): If True, print more details to STDOUT. Defaults to False.
    """
    print_green(f"[bold green]{os.path.realpath(infile)}")
    if not no_details:
        checksum = calculate_md5(infile)
        date_created = get_file_creation_date(infile)
        bytesize = get_file_size(infile)
        line_count = get_line_count(infile)
        console.print(f"[blue]md5sum:[/] {checksum}")
        console.print(f"[blue]date-created/modified:[/] {date_created}")
        console.print(f"[blue]size:[/] {bytesize}")
        console.print(f"[blue]line-count:[/] {line_count}")


def find_most_recent_version_directory(directory: str, dir_pattern: str) -> Optional[str]:
    """Find the most recent version directory in the specified directory pattern.

    Args:
        directory (str): The directory to search for the most recent version directory.
        dir_pattern (str): The directory pattern to filter for.

    Returns:
        str: The most recent version directory.
    """
    # Get a list of all files in the directory
    all_files = os.listdir(directory)

    if not all_files:
        console.print(f"Directory '{directory}' is empty.")
        return None

    # Create a dictionary to store file paths and their creation times
    dir_times = {}

    if dir_pattern:
        # Filter files based on the provided pattern and extension
        matching_dirs = [file for file in all_files if re.match(dir_pattern, file)]
    else:
        matching_dirs = [file for file in all_files]


    if not matching_dirs:
        console.print(f"No matching directories found in directory '{directory}'.")
        return None

    for dir in matching_dirs:
        dir_path = os.path.join(directory, dir)

        # Check if it's a dir (not a directory)
        if os.path.isdir(dir_path):
            # Get the dir creation time (Linux timestamp)
            creation_time = os.path.getctime(dir_path)
            # Store the dir path and creation time in the dictionary
            dir_times[dir_path] = creation_time

    if not dir_times:
        console.print(f"No valid dirs found in the directory '{directory}'.")
        return None

    # Find the dir with the highest creation time
    most_recent_dir = max(dir_times, key=dir_times.get)

    return most_recent_dir


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
@click.option('--config_file', type=click.Path(exists=True), help=f"Optional: The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'.")
@click.option('--indir', help="Optional: The input directory to check for assets.")
@click.option('--logfile', help="Optional: The log file")
@click.option('--no_details', is_flag=True, help=f"Optional: If specified, will not show file details - default is '{DEFAULT_NO_DETAILS}'")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output final report file")
@click.option('--pattern', help="Optional: the filename pattern to filter for")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: Optional[str], indir: str, logfile: Optional[str], no_details: Optional[bool], outdir: Optional[str], outfile: Optional[str], pattern: Optional[str], verbose: Optional[bool]):
    """Find most recent set of assets in specified directory.

    Args:
        config_file (Optional[str]): The configuration file for this project.
        indir (str): The input directory to check for assets.
        logfile (Optional[str]): The log file.
        no_details (Optional[bool]): If specified, will not show file details.
        outdir (Optional[str]): The output directory.
        outfile (Optional[str]): The output final report file.
        pattern (Optional[str]): The filename pattern to filter for.
        verbose (Optional[bool]): Will print more info to STDOUT.
    """
    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    if indir is None:
        indir = os.path.abspath(os.getcwd())
        print_yellow(f"--indir was not specified and therefore was set to '{indir}'")

    if no_details is None:
        no_details = DEFAULT_NO_DETAILS
        print_yellow(f"--no_details was not specified and therefore was set to '{no_details}'")

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

    logging.info(f"{indir=}")
    item = find_most_recent_version_directory(
        directory=indir,
        dir_pattern=pattern,
    )
    if item is not None:
        console.print(f"Found this latest directory: {item}")
        profile_directory(item, no_details=no_details)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()

