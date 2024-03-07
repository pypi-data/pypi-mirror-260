"""Archive a directory in-place."""
import click
import os
import subprocess
import sys

from datetime import datetime
from rich.console import Console

from .file_utils import check_indir_status

error_console = Console(stderr=True, style="bold red")

console = Console()


def archive_directory(directory_path: str) -> None:
    """Archive a directory in-place.

    Args:
        directory_path (str): the directory to be archived in-place
    """
    # Get the base name of the target directory
    current_dir = os.getcwd()
    dirname = os.path.dirname(directory_path)
    os.chdir(dirname)

    base_name = os.path.basename(directory_path)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    # Create the target filename with .tgz extension
    target_filename = f"{base_name}_{timestamp}.tgz"

    # Build the tar command
    tar_command = ["tar", "zcvf", target_filename, base_name]

    try:
        # Execute the tar command using subprocess
        subprocess.run(tar_command, check=True)
        print(f"Directory '{directory_path}' successfully archived to '{target_filename}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    os.chdir(current_dir)


@click.command()
@click.argument('indir', type=str, required=True)
def main(indir: str):
    """Archive a directory in-place.

    Args:
        indir (str): the directory to be archived in-place
    """

    error_ctr = 0

    if indir is None:
        error_console.print(f"Usage: {os.path.basename(__file__)} dir")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_indir_status(indir)

    archive_directory(indir)


if __name__ == "__main__":
    main()
