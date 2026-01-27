"""Command-line interface for the fastqc-summary app.

Typical usage examples:
    >>> import zipfile
    >>> from fastqc_summary.cli import get_args
    >>> args = get_args()
    >>> with zipfile.ZipFile(args.fastqc_archive, "r") as zf:
    >>>     files = zf.namelist()
"""

import argparse
from pathlib import Path
from typing import NamedTuple
import zipfile


class Args(NamedTuple):
    """Command-line arguments."""
    fastqc_archive: str


def get_args(argv: list[str] | None = None) -> Args:
    """Get command-line arguments.

    Get and validate command line arguments.

    Args:
        argv: A list of args to explicitly supply to the parser. Intended for testing only. Leave as None for typical usage.

    Returns:
        An instance of an Args NamedTuple object.

    Raises:
        SystemExit: A required argument was not provided or other fatal error occurred during argument parsing.
        FileNotFoundError: Input file could not be found.
        BadZipFile: Input file was not a valid ZIP file.
    """
    parser = argparse.ArgumentParser(
        description="CLI app that summarizes FastQC results.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "fastqc_archive",
        type=str,
        help="Path to FastQC ZIP archive file. This is the '_fastqc.zip' file written by FastQC.",
    )

    args = parser.parse_args(argv)

    # validate the FastQC ZIP archive file
    if not Path(args.fastqc_archive).exists():
        raise FileNotFoundError(f"FastQC archive file '{args.fastqc_archive}' could not be found.")
    if not zipfile.is_zipfile(args.fastqc_archive):
        raise zipfile.BadZipFile(f"FastQC archive file '{args.fastqc_archive}' is not a valid ZIP file.")

    return Args(fastqc_archive=args.fastqc_archive)
