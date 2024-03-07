"""Delete user's old files and directories."""
import shutil
import datetime
import pwd
import os
import sys
import click
import pathlib
import logging

from datetime import datetime, timedelta
from rich.console import Console
from typing import Optional, List

from .file_utils import check_indir_status

DEFAULT_PROJECT = "data-file-utils"

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    "delete-users-old-files-and-directories",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_USERNAME = os.getenv("USER")

DEFAULT_NO_TEST_MODE = True

DEFAULT_INDIR = "/tmp"

DEFAULT_DAYS_OLD = 2

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def delete_files_created_by_user(
        logfile: str,
        outfile: str = DEFAULT_OUTDIR,
        directory: str = DEFAULT_INDIR,
        username: str = DEFAULT_USERNAME,
        days_ago: int = DEFAULT_DAYS_OLD,
        no_test: bool = DEFAULT_NO_TEST_MODE,
        verbose: bool = DEFAULT_VERBOSE):
    """Delete files and directories that belong to the specified user and were created more than the specified number of days ago.

    Args:
        directory (str, optional): The directory to check for old files belonging to the specified user. Defaults to DEFAULT_INDIR.
        username (str, optional): The user that owns old files and directories to be deleted. Defaults to DEFAULT_USERNAME.
        days_ago (int, optional): The minimum number of days ago that the files or directories were created. Defaults to DEFAULT_DAYS_OLD.
        no_test (bool, optional): If True, will not delete files and directories.  If False, will delete files and directories. Defaults to DEFAULT_NO_TEST_MODE.
        verbose (bool, optional): If True, will print more info to STDOUT.  If False, will not print more info to STDOUT. Defaults to DEFAULT_VERBOSE.
    """
    if verbose:
        print(f"Will attempt to identify and delete all files and subdirectories that belong to username '{username}' that are older than '{days_ago}' days old")
    logging.info(f"Will attempt to identify and delete all files and subdirectories that belong to username '{username}' that are older than '{days_ago}' days old")

    cutoff_time = datetime.now() - timedelta(days=days_ago)

    file_ctr = 0
    file_deleted_ctr = 0
    dir_ctr = 0
    dir_deleted_ctr = 0
    something_else_ctr = 0
    recent_file_ctr = 0
    recent_dir_ctr = 0
    recent_something_else_ctr = 0
    other_user_ctr = 0

    delete_files_list = []
    delete_dirs_list = []

    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            path = os.path.join(root, name)
            stat_info = os.stat(path)

            user_info = pwd.getpwuid(stat_info.st_uid)

            if user_info.pw_name != username:
                other_user_ctr += 1
                continue

            if os.path.isfile(path):
                file_ctr += 1
            elif os.path.isdir(path):
                dir_ctr += 1
            else:
                something_else_ctr += 1
                continue

            # Check if the item belongs to the specified user and was created 2 days ago
            # if os.path.exists(path) and stat_info.st_uid == os.getpwnam(username).pw_uid and datetime.datetime.fromtimestamp(stat_info.st_ctime) < cutoff_time:
            try:
                if datetime.fromtimestamp(stat_info.st_ctime) < cutoff_time:
                    if verbose:
                        print(f"Found user item '{path}'")
                    logging.info(f"Found user item '{path}'")

                    try:
                        if os.path.isfile(path):
                            if no_test:
                                os.remove(path)
                                if verbose:
                                    print(f"Deleted file: {path}")
                                logging.info(f"Deleted file: {path}")
                            else:
                                if verbose:
                                    print(f"Running in test mode - so will not deleted file: {path}")
                                logging.info(f"Running in test mode - so will not delete file: {path}")
                            delete_files_list.append(path)
                            file_deleted_ctr += 1

                        elif os.path.isdir(path):
                            if no_test:
                                shutil.rmtree(path)
                                if verbose:
                                    print(f"Deleted directory: {path}")
                                logging.info(f"Deleted directory: {path}")
                            else:
                                if verbose:
                                    print(f"Running in test mode - so will not delete directory: {path}")
                                logging.info(f"Running in test mode - so will not delete directory: {path}")
                            dir_deleted_ctr += 1
                            delete_dirs_list.append(path)

                    except Exception as e:
                        print(f"Error deleting {path}: {e}")
                        logging.error(f"Error deleting {path}: {e}")
                else:
                    if os.path.isfile(path):
                        recent_file_ctr += 1
                    elif os.path.isdir(path):
                        recent_dir_ctr += 1
                    else:
                        recent_something_else_ctr += 1

            except KeyError:
                print(f"User with UID {stat_info.st_uid} not found.")
                logging.error(f"User with UID {stat_info.st_uid} not found.")

    if verbose:
        print(f"Ignored '{other_user_ctr}' items that belong to some other user")

        print(f"Number of files analyzed '{file_ctr}'")

        print(f"Number of directories analyzed '{dir_ctr}'")

        print(f"Number of items analyzed that are neither files nor directories '{something_else_ctr}'")

        if no_test:
            print(f"Was running in test mode - so did not actually attempt to delete items belonging to user '{username}'")

        print(f"Number of files deleted '{file_deleted_ctr}'")

        print(f"Number of directories deleted '{dir_deleted_ctr}'")

        print(f"Number of files that are too recent to be deleted '{recent_file_ctr}'")

        print(f"Number of directories that are too recent to be deleted '{recent_dir_ctr}'")

        print(f"Number of items that are neither files nor directories that are too recent to be deleted '{recent_something_else_ctr}'")


    logging.info(f"Ignored '{other_user_ctr}' items that belong to some other user")

    logging.info(f"Number of files analyzed '{file_ctr}'")

    logging.info(f"Number of directories analyzed '{dir_ctr}'")

    logging.info(f"Number of items analyzed that are neither files nor directories '{something_else_ctr}'")

    if no_test:
        logging.info(f"Was running in test mode - so did not actually attempt to delete items belonging to user '{username}'")

    logging.info(f"Number of files deleted '{file_deleted_ctr}'")

    logging.info(f"Number of directories deleted '{dir_deleted_ctr}'")

    logging.info(f"Number of files that are too recent to be deleted '{recent_file_ctr}'")

    logging.info(f"Number of directories that are too recent to be deleted '{recent_dir_ctr}'")

    logging.info(f"Number of items that are neither files nor directories that are too recent to be deleted '{recent_something_else_ctr}'")

    generate_report(
        no_test,
        days_ago,
        directory,
        logfile,
        username,
        delete_files_list,
        delete_dirs_list,
        outfile)


def generate_report(
        no_test: bool,
        days: int,
        indir: str,
        logfile: str,
        username: str,
        delete_files_list: List[str],
        delete_dirs_list: List[str],
        outfile: str = None):
    """Generate a report of the files and directories that were deleted.

    Args:
        no_test (bool): If True, will not delete files and directories.  If False, will delete files and directories.
        days (int): The minimum number of days ago that the files or directories were created.
        indir (str): The directory to check for old files belonging to the specified user.
        logfile (str): The log file.
        username (str): The user that owns old files and directories to be deleted.
        delete_files_list (List[str]): The list of files that were deleted.
        delete_dirs_list (List[str]): The list of directories that were deleted.
        outfile (str, optional): The output report file. Defaults to None.
    """
    with open(outfile, 'w') as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## indir: {indir}\n")
        of.write(f"## logfile: {logfile}\n")
        of.write(f"## username: {username}\n")
        of.write(f"## days-old: {days}\n")
        of.write(f"## no-test-mode: {no_test}\n")

        if len(delete_files_list) > 0:
            if no_test:
                of.write(f"## Deleted the following '{len(delete_files_list)}' files:\n")
            else:
                of.write(f"## Would have deleted the following '{len(delete_files_list)}' files:\n")
            for i, file in enumerate(delete_files_list, start=1):
                of.write(f"{i}. {file}\n")

        if len(delete_dirs_list) > 0:
            if no_test:
                of.write(f"## Deleted the following '{len(delete_dirs_list)}' directoriess:\n")
            else:
                of.write(f"## Would have deleted the following '{len(delete_dirs_list)}' directories:\n")
            for i, dir in enumerate(delete_dirs_list, start=1):
                of.write(f"{i}. {dir}\n")

    logging.info(f"Wrote file report file '{outfile}'")
    print(f"Wrote file report file '{outfile}'")


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


def validate_no_test_mode(ctx, param, value):
    """Validate the no_test flag.

    Args:
        ctx (Context): The click context.
        param (str): The parameter name.
        value (bool): The value of the parameter.

    Returns:
        bool: The value of the parameter.
    """
    if value is None:
        click.secho("--no_test was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_NO_TEST_MODE
    # else:
    #     print(value)
    return value


@click.command()
@click.option('--days', help=f"Optional: The number of days ago that files were created that should be deleted - default is '{DEFAULT_DAYS_OLD}'")
@click.option('--indir', help=f"Optional: The directory to search for old user's files - default is '{DEFAULT_INDIR}'")
@click.option('--logfile', help="Optional: The log file")
@click.option('--no-test', is_flag=True, help=f"Optional: If specified, will actually delete files and directories - default is '{DEFAULT_NO_TEST_MODE}'", callback=validate_no_test_mode)
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output report file")
@click.option('--username', help=f"Optional: The username of the account whose old files should be deleted - default is '{DEFAULT_USERNAME}'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(days: Optional[int], indir: Optional[str], logfile: Optional[str], no_test: Optional[bool], outdir: Optional[str], outfile: Optional[str], username: Optional[str], verbose: Optional[bool]):
    """Delete user's old files.

    Args:
        days (Optional[int]): The number of days ago that files were created that should be deleted.
        indir (Optional[str]): The directory to search for old user's files.
        logfile (Optional[str]): The log file.
        no_test (Optional[bool]): If specified, will actually delete files and directories.
        outdir (Optional[str]): The output directory.
        outfile (Optional[str]): The output report file.
        username (Optional[str]): The username of the account whose old files should be deleted.
        verbose (Optional[bool]): Will print more info to STDOUT.
    """

    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if indir is None:
        indir = DEFAULT_INDIR
        console.print(f"[yellow]--indir was not specified and therefore was set to '{indir}'[/]")

    check_indir_status(indir)

    if username is None:
        username = DEFAULT_USERNAME
        console.print(f"[yellow]--username was not specified and therefore was set to '{username}'[/]")

    if no_test is None:
        no_test = DEFAULT_NO_TEST_MODE
        console.print(f"[yellow]--no_test was not specified and therefore was set to '{no_test}'[/]")

    if days is None:
        days = DEFAULT_DAYS_OLD
        console.print(f"[yellow]--days was not specified and therefore was set to '{days}'[/]")

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
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.report.txt'
        )
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        console.print(f"[yellow]--verbose was not specified and therefore was set to '{verbose}'[/]")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    if not no_test:
        print("Running in test mode.\nWill not actually delete files and directories.\nTry --no-test to actually delete files and directories ")
    else:
        print("Will actually delete files and directories")

    delete_files_created_by_user(
        logfile,
        outfile,
        indir,
        username,
        days,
        no_test,
        verbose,
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")
    sys.exit(0)

if __name__ == "__main__":
    main()

