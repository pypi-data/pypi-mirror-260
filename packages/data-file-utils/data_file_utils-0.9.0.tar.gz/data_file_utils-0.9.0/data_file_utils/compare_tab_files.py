"""Compare two sorted review files line-by-line and column-by-column."""
import click
import logging
import os
import pathlib
import sys

import xlsxwriter

from typing import Dict, Optional
from datetime import datetime
from rich.console import Console

from file_utils import check_infile_status


DEFAULT_PROJECT = 'data-file-utils'

DEFAULT_IGNORE_COLUMNS = False

HEADER_LINE = 1
RECORDS_START_LINE = 2
MAX_COLUMN_COUNT = 0

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_OUTFILE = os.path.join(
    DEFAULT_OUTDIR,
    os.path.splitext(os.path.basename(__file__))[0] + '.diff.txt'
)


DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.json'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def get_column_number_to_column_letters_lookup(max_column_number: int = MAX_COLUMN_COUNT) -> Dict[int, str]:
    """Get a lookup of column numbers to column letters.

    Args:
        max_column_number (int, optional): The maximum number of columns. Defaults to MAX_COLUMN_COUNT.

    Returns:
        Dict[int, str]: The lookup of column numbers to column letters.
    """
    column_numbers = [x for x in range(max_column_number)]
    lookup = {}
    for column_number in column_numbers:
        column_letter = xlsxwriter.utility.xl_col_to_name(column_number)
        column_number += 1
        logging.debug(f"Converted column number '{column_number}' to column letter '{column_letter}'")
        lookup[column_number] = column_letter
    return lookup


def read_file(file_path: str):
    """Read a tab-delimited file and return its content as a list of lists.

    Args:
        file_path (str): The path to the file to be read.
    """
    logging.info(f"Going to read file '{file_path}'")
    with open(file_path, 'r', encoding="latin-1") as file:
        lines = file.readlines()
    header = lines[HEADER_LINE].strip().split('\t')
    header_index_to_name_lookup = {}
    header_name_to_index_lookup = {}
    for i, h in enumerate(header):
        header_index_to_name_lookup[i] = h
        header_name_to_index_lookup[h] = i
    data = [line.strip().split('\t') for line in lines[RECORDS_START_LINE:]]
    return header, header_index_to_name_lookup, header_name_to_index_lookup, data

def get_ignore_columns_lookup(ignore_columns_str: str) -> Dict[str, bool]:
    ignore_columns_lookup = {}
    logging.info(f"Will ignore columns: {ignore_columns_str}")
    columns = ignore_columns_str.split(",")
    for column in columns:
        ignore_columns_lookup[column.strip()] = True
    return ignore_columns_lookup


def compare_files(file1_path: str, file2_path: str, ignore_columns: bool, ignore_columns_str: Optional[str]):
    """Compare two tab-delimited files and store differences.

    Args:
        file1_path (str): The path to the first file to be compared.
        file2_path (str): The path to the second file to be compared.
        ignore_columns (bool): Whether to ignore columns.
        ignore_columns_str (Optional[str]): The comma-separated list of columns to be ignored.
    """
    header1, header_index_to_name_lookup1, header_name_to_index_lookup1, data1 = read_file(file1_path)
    header2, header_index_to_name_lookup2, header_name_to_index_lookup2, data2 = read_file(file2_path)

    if ignore_columns:
        ignore_columns_lookup = get_ignore_columns_lookup(ignore_columns_str)

    # if header1 != header2:
    #     print("Headers of the two files are different.")
    #     return

    logging.info("Going to compare contents of the two files now")

    max_rows = max(len(data1), len(data2))
    differences = []
    max_max_columns = 0

    for i in range(1, max_rows + 1):
        if i <= len(data1):
            row1 = data1[i - 1]
        else:
            row1 = [""] * len(header1)

        if i <= len(data2):
            row2 = data2[i - 1]
        else:
            row2 = [""] * len(header2)

        max_columns = max(len(row1), len(row2))
        if max_columns > max_max_columns:
            max_max_columns = max_columns

        # max_columns = 59

        for j in range(0, max_columns):

            cell1 = row1[j] if j < len(row1) else ""
            cell2 = row2[j] if j < len(row2) else ""

            if cell1 != cell2:
                if ignore_columns and j in header_index_to_name_lookup1 and header_index_to_name_lookup1[j] in ignore_columns_lookup:
                    logging.info(f"Found differences in cell 1 '{cell1}' and cell 2 '{cell2}' but will ignore")
                    continue
                # logging.info(f"i '{i}' j '{j}' max_columns '{max_columns}' max_rows '{max_rows}' cell1 '{cell1}' cell2 '{cell2}'")
                differences.append((i, header1[j] if j < len(header1) else header2[j], j + 1, cell1, cell2))

    global MAX_COLUMN_COUNT
    MAX_COLUMN_COUNT = max_max_columns
    return differences



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
@click.option('--ignore_columns', is_flag=True, help=f"Optional: Ignore columns specified in --ignore_columns_str - default is '{DEFAULT_IGNORE_COLUMNS}'")
@click.option('--ignore_columns_str', help="Optional: comma-separated list of column headers wrapped in quotes")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help=f"Optional: The output file to which differences will be written to - default is '{DEFAULT_OUTFILE}'")
@click.option('--tab_file_1', help="Required: The first sorted review file (.tsv)")
@click.option('--tab_file_2', help="Required: The second sorted review file (.tsv)")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(ignore_columns: Optional[bool], ignore_columns_str: Optional[str], logfile: Optional[str], outdir: Optional[str], outfile: Optional[str], tab_file_1: str, tab_file_2: str, verbose: Optional[bool]):
    """Compare two sorted review files line-by-line and column-by-column."""

    error_ctr = 0

    if tab_file_1 is None:
        error_console.print("--tab_file_1 was not specified")
        error_ctr += 1

    if tab_file_2 is None:
        error_console.print("--tab_file_2 was not specified")
        error_ctr += 1

    if error_ctr > 0:
        error_console.print("Required command-line arguments were not provided")
        sys.exit(1)

    check_infile_status(tab_file_1)
    check_infile_status(tab_file_2)

    if ignore_columns is None:
        ignore_columns = DEFAULT_IGNORE_COLUMNS
        console.print(f"[yellow]--ignore_columns was not specified and therefore was set to '{ignore_columns}'[/]")


    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")

    if outfile is None:
        outfile = DEFAULT_OUTFILE
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if ignore_columns:
        if ignore_columns_str is None:
            console.print(f"[bold red]--ignore_columns was specified but --ignore_columns_str was not specified[/]")
            sys.exit(-1)

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    differences = compare_files(
        tab_file_1,
        tab_file_2,
        ignore_columns,
        ignore_columns_str
    )

    if differences:
        print(f"[bold red]{len(differences)} differences found[/]")
        logging.info(f"{len(differences)} differences found")

        lookup = get_column_number_to_column_letters_lookup(MAX_COLUMN_COUNT)

        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## tab-delimited file 1: {tab_file_1}\n")
            of.write(f"## tab-delimited file 2: {tab_file_2}\n")
            of.write(f"## logfile: {logfile}\n")

            of.write("Line #\tColumn Name\tColumn #\tColumn Letter\tValue in File 1\tValue in File 2\n")
            for diff in differences:
                excel_column_letters = lookup[diff[2]]
                of.write(f"{diff[0]}\t{diff[1]}\t{diff[2]}\t{excel_column_letters}\t{diff[3]}\t{diff[4]}\n")

        logging.info(f"Wrote differences to output file '{outfile}'")
        if verbose:
            print(f"Wrote differences to output file '{outfile}'")

    else:
        print("[green]No differences found.[/]")
        logging.info("No differences found.")

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
