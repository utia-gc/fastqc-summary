import sys


def printerr(e: str, exit_status: int = 1) -> None:
    """Print error message and exit.

    Print an error message to stderr, and exit with the given exit status.

    Args:
        e: An error message.
        exit_status: An exit status to return.
    """
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(exit_status)
