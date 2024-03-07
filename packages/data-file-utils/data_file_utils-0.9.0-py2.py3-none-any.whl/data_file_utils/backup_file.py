"""Backup a file."""
import os
import sys
import click
import shutil

from datetime import datetime
from rich.console import Console

from .file_utils import check_infile_status

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))


error_console = Console(stderr=True, style="bold red")

console = Console()


@click.command()
@click.argument('infile', type=str, required=True)
def main(infile: str):
    """Backup a file in-place.

    Args:
        infile (str): The file to be backed up in-place.
    """

    error_ctr = 0

    if infile is None:
        error_console.print(f"Usage: {os.path.basename(__file__)} infile")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_infile_status(infile)

    dirname = os.path.dirname(infile)
    bakfile = os.path.join(
        dirname,
        os.path.basename(infile) + f".{DEFAULT_TIMESTAMP}.bak"
    )

    shutil.copyfile(infile, bakfile)
    print(f"Backed-up '{infile}' to '{bakfile}'")


if __name__ == "__main__":
    main()
