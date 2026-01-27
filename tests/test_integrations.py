"""Test integrations at level of app main entry point function and CLI.

Integration tests of the full CLI app are mainly smoke tests, i.e. check that the app is installable and runs.
Note that the app must be installed in order to run the CLI integration tests, e.g. by `uv sync` and using `uv` to launch the test.

Most of the precise integration testing is performed at the level of the main function.
This allows for easier, faster, and more precise control of test cases.

Typical usage examples:
    $ uv sync
    $ uv run pytest tests/test_integrations.py
"""

import subprocess

from fastqc_summary import main


class TestIntegrationCLI:
    """Integration testing at the CLI level.

    These are smoke tests to ensure the CLI app is installable and runs.
    Keep these tests short and sweet, and focus on making sure the app succeeds and fails where expected.
    """

    def test_no_args(self) -> None:
        result = subprocess.run(
            ["fastqc-summary"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert result.stdout.strip() == "Hello from fastqc-summary!"


class TestIntegrationMain:
    """Integration testing at main function level.

    The entrypoint for the CLI app is the `main()` method in the package root `__init__.py` module.
    Most of the precise app functionality is tested at this stage since it is faster and easier to mock here than it is to run the CLI.
    Test end-to-end functionality, expected failures, and edge cases here.
    """

    def test_no_cli_args(self, capsys) -> None:
        main()
        captured = capsys.readouterr()

        assert captured.out == "Hello from fastqc-summary!\n"
