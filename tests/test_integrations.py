"""Test integrations at level of app main entry point function and CLI.

Integration tests of the full CLI app are mainly smoke tests, i.e. check that the app is installable and runs.
Note that the app must be installed in order to run the CLI integration tests, e.g. by `uv sync` and using `uv` to launch the test.

Most of the precise integration testing is performed at the level of the main function.
This allows for easier, faster, and more precise control of test cases.

Typical usage examples:
    $ uv sync
    $ uv run pytest tests/test_integrations.py
"""

import json
import subprocess
from unittest.mock import patch

import pytest

from fastqc_summary import main


class TestIntegrationCLI:
    """Integration testing at the CLI level.

    These are smoke tests to ensure the CLI app is installable and runs.
    Keep these tests short and sweet, and focus on making sure the app succeeds and fails where expected.
    """

    def test_no_args_prints_usage(self) -> None:
        result = subprocess.run(
            ["fastqc-summary"],
            capture_output=True,
            text=True,
        )

        assert result.returncode > 0
        assert result.stderr.startswith("usage: fastqc-summary")


class TestIntegrationMain:
    """Integration testing at main function level.

    The entrypoint for the CLI app is the `main()` method in the package root `__init__.py` module.
    Most of the precise app functionality is tested at this stage since it is faster and easier to mock here than it is to run the CLI.
    Test end-to-end functionality, expected failures, and edge cases here.
    """

    @pytest.mark.parametrize("test_argv, read_count, base_count", [
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "-o"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "--output"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "-o"],
            0,
            0
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "--output"],
            0,
            0
        ),
    ])
    def test_succeeds_output_file(self, tmp_path, test_argv, read_count, base_count) -> None:
        expected_summary_output = {
            "read_count": read_count,
            "base_count": base_count,
        }

        # construct the output file and add to args
        output_path = tmp_path / "output.json"
        test_argv.append(str(output_path))

        # mock args for testing main
        with patch("sys.argv", test_argv):
            main()

            # check output file written
            assert output_path.exists()
            # check output file has expected summaries
            with open(output_path, "r") as output_json:
                actual_summary_output = json.load(output_json)
                assert actual_summary_output == expected_summary_output


    @pytest.mark.parametrize("test_argv, read_count, base_count", [
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip"],
            0,
            0
        ),
    ])
    def test_succeeds_missing_outputs_stdout(self, capsys, test_argv, read_count, base_count) -> None:
        expected_summary_output = {
            "read_count": read_count,
            "base_count": base_count,
        }

        # mock args for testing main
        with patch("sys.argv", test_argv):
            main()
            captured = capsys.readouterr()

            # check output file expected summaries directed to stdout
            print(captured.out)
            actual_summary_output = json.loads(captured.out)
            assert actual_summary_output == expected_summary_output


    @pytest.mark.parametrize("test_argv, read_count, base_count", [
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "-o", "-"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "--output", "-"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "-o", "-"],
            0,
            0
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "--output", "-"],
            0,
            0
        ),
    ])
    def test_succeeds_hyphen_outputs_stdout(self, capsys, test_argv, read_count, base_count) -> None:
        expected_summary_output = {
            "read_count": read_count,
            "base_count": base_count,
        }

        # mock args for testing main
        with patch("sys.argv", test_argv):
            main()
            captured = capsys.readouterr()

            # check output file expected summaries directed to stdout
            actual_summary_output = json.loads(captured.out)
            assert actual_summary_output == expected_summary_output


    @pytest.mark.parametrize("test_argv, read_count, base_count", [
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "-o", "/dev/stdout"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/SRR1067505_1_fastqc.zip", "--output", "/dev/stdout"],
            18361776,
            661023936
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "-o", "/dev/stdout"],
            0,
            0
        ),
        (
            ["fastqc-summary", "tests/data/empty_fastqc.zip", "--output", "/dev/stdout"],
            0,
            0
        ),
    ])
    def test_succeeds_dev_stdout_outputs_stdout(self, capsys, test_argv, read_count, base_count) -> None:
        expected_summary_output = {
            "read_count": read_count,
            "base_count": base_count,
        }

        # mock args for testing main
        with patch("sys.argv", test_argv):
            main()
            captured = capsys.readouterr()

            # check output file expected summaries directed to stdout
            actual_summary_output = json.loads(captured.out)
            assert actual_summary_output == expected_summary_output
