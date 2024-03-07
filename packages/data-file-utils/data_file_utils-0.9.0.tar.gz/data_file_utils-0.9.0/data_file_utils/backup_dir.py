"""Backup a file."""
import os
import sys
import click
import shutil

from datetime import datetime
from rich.console import Console

from .file_utils import check_indir_status

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))


error_console = Console(stderr=True, style="bold red")

console = Console()


@click.command()
@click.argument('indir', type=str, required=True)
def main(indir: str):
    """Backup a directory in-place.

    Args:
        indir (str): The directory to be backed up in-place.
    """

    error_ctr = 0

    if indir is None:
        error_console.print(f"Usage: {os.path.basename(__file__)} dir")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_indir_status(indir)

    bakdir = os.path.join(indir + f".{DEFAULT_TIMESTAMP}.bak")

    shutil.copytree(indir, bakdir)
    print(f"Backed-up '{indir}' to '{bakdir}'")


if __name__ == "__main__":
    main()
