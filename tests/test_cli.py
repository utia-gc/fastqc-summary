from pathlib import Path
import zipfile

import pytest

from fastqc_summary.cli import Args, get_args


class TestCLIFastqcArchive:
    """Test behavior of FastQC archive argument."""

    @pytest.mark.parametrize("files, test_argv, fastqc_archive", [
        # create a FastQC archive
        (
            {"test/fastqc_data.txt": "##FastQC\t0.12.1"},
            [],
            None
        ),
        # use a FastQC archive from the SRR test FastQC archive
        (
            {},
            [],
            "tests/data/SRR1067505_1_fastqc.zip"
        ),
        # use a FastQC archive from the empty test FastQC archive
        (
            {},
            [],
            "tests/data/empty_fastqc.zip"
        ),
    ])
    def test_succeeds_fastqc_archive(self, create_zip, files, test_argv, fastqc_archive) -> None:
        if not fastqc_archive and files:
            fastqc_archive = create_zip(files)

        test_argv.append(str(fastqc_archive))

        args = get_args(test_argv)

        assert args.fastqc_archive == str(fastqc_archive)
        assert Path(args.fastqc_archive).exists()
        assert zipfile.is_zipfile(args.fastqc_archive)


    @pytest.mark.parametrize("test_argv", [
        ([]),
    ])
    def test_fail_no_fastqc_archive(self, test_argv) -> None:
        with pytest.raises(SystemExit):
            get_args(test_argv)


    @pytest.mark.parametrize("test_argv", [
        (["test_fastqc.zip"]),
    ])
    def test_fail_fastqc_archive_file_does_not_exist(self, test_argv) -> None:
        with pytest.raises(FileNotFoundError, match="FastQC archive file 'test_fastqc.zip' could not be found."):
            get_args(test_argv)


    @pytest.mark.parametrize("test_argv", [
        ([]),
    ])
    def test_fail_fastqc_archive_file_not_zip_file(self, tmp_path, test_argv) -> None:
        # create a FastQC data file and add it to the arguments list
        fastqc_data_file = tmp_path / "fastqc_data.txt"
        fastqc_data_file.write_text("##FastQC\t0.12.1")
        test_argv.append(str(fastqc_data_file))

        with pytest.raises(zipfile.BadZipFile, match="FastQC archive file '.*' is not a valid ZIP file."):
            get_args(test_argv)
