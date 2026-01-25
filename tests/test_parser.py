import io
from pathlib import Path
import zipfile

import pytest

from fastqc_summary.parser import (
    find_fastqc_data_file,
    parse_modules,
    Module,
)


class TestParseModules:
    """Test parse_modules()."""

    @pytest.mark.parametrize("fastqc_zip_path", [
        ("tests/data/SRR1067505_1_fastqc.zip"),
    ])
    def test_parse_modules_yields_modules(self, fastqc_zip_path) -> None:
        modules = parse_modules(fastqc_zip_path)

        for module in modules:
            assert isinstance(module, Module)


    @pytest.mark.parametrize("fastqc_zip_path", [
        ("tests/data/SRR1067505_1_fastqc.zip"),
    ])
    def test_parse_modules_yields_basic_stats(self, fastqc_zip_path) -> None:
        modules = parse_modules(fastqc_zip_path)
        basic_stats_module = next(modules)

        assert basic_stats_module.name == "Basic Statistics"
        assert basic_stats_module.status == "pass"
        assert basic_stats_module.columns == ["Measure", "Value"]
        assert any(data_row.startswith("Total Sequences\t") for data_row in basic_stats_module.data)


class TestFindFastqcDataFile:
    """Test find_fastqc_data_file()."""

    @pytest.mark.parametrize("fastqc_zip_path,expected_data_file", [
        ("tests/data/SRR1067505_1_fastqc.zip", "SRR1067505_1_fastqc/fastqc_data.txt"),
    ])
    def test_find_fastqc_data_success(self, fastqc_zip_path, expected_data_file) -> None:
        fastqc_zip_file = zipfile.ZipFile(fastqc_zip_path)
        fastqc_data_file = find_fastqc_data_file(fastqc_zip_file)
        assert fastqc_data_file == expected_data_file


    def test_find_fastqc_data_no_file(self) -> None:
        # Create an in-memory zip with no fastqc_data.txt
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("other_file.txt", "some data")
            zf.writestr("data.csv", "more data")

        zip_buffer.seek(0)
        with zipfile.ZipFile(zip_buffer) as archive:
            with pytest.raises(FileNotFoundError, match="fastqc_data.txt not found in archive"):
                find_fastqc_data_file(archive)


    def test_find_fastqc_data_multiple_files(self) -> None:
        # Create an in-memory zip with multiple fastqc_data.txt files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("sample1/fastqc_data.txt", "sample1 data")
            zf.writestr("sample2/fastqc_data.txt", "sample2 data")

        zip_buffer.seek(0)
        with zipfile.ZipFile(zip_buffer) as archive:
            with pytest.raises(ValueError, match="Multiple fastqc_data.txt files found in archive: "):
                find_fastqc_data_file(archive)
