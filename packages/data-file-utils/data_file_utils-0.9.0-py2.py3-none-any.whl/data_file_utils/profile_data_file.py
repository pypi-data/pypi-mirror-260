"""Profile the specified file."""
import os
import sys
import click

from rich.console import Console

from file_utils import check_infile_status, calculate_md5, get_file_creation_date, get_file_size, get_line_count


error_console = Console(stderr=True, style="bold red")

console = Console()


@click.command()
@click.argument('infile', type=str, required=True)
def main(infile: str):
    """Profile data file.

    Args:
        infile (str): The input file to profile.
    """

    error_ctr = 0

    if infile is None:
        error_console.print(f"Usage: {os.path.basename(__file__)} infile")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile)

    md5sum = calculate_md5(infile)
    create_date = get_file_creation_date(infile)
    file_size = get_file_size(infile)
    line_count = get_line_count(infile)

    print(f"File: {os.path.abspath(infile)}")
    print(f"md5sum: {md5sum}")
    print(f"create_date: {create_date}")
    print(f"byte_size: {file_size}")
    print(f"line_count: {line_count}")


if __name__ == "__main__":
    main()
