"""Create a temporary directory."""
import os
import pathlib

from datetime import datetime

DEFAULT_USERNAME = os.environ.get("USER", None)

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))


def main():
    """Create a temporary directory."""

    root = input("Enter the root directory: [/tmp]: ")
    if root == "":
        root = "/tmp"
    root = root.strip()

    userdir = input(f"Enter the user directory: [{DEFAULT_USERNAME}]: ")
    if userdir is None or userdir == "":
        userdir = DEFAULT_USERNAME
    if userdir is not None:
        userdir = userdir.strip()

    purpose = None
    while purpose is None or purpose == "":
        purpose = input("Enter the purpose of the directory: ")
        purpose = purpose.strip().replace(" ", "_")

    outdir = os.path.join(root, userdir, purpose, DEFAULT_TIMESTAMP)

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print(f"Created output directory '{outdir}'")


if __name__ == "__main__":
    main()
