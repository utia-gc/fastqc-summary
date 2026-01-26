import pytest

from fastqc_summary.parser import Module
from fastqc_summary.summaries import (
    summarize_base_count,
    summarize_read_count,
)


class TestSummarizeReadCount:
    @pytest.mark.parametrize("basic_stats_module, expected_read_count", [
        ("basic_stats_empty", 0),
        ("basic_stats_sra_data", 18361776),
        ("basic_stats_ngs_test", 50000),
    ])
    def test_summarize_read_count_succeeds_well_formed_data(self, request, basic_stats_module, expected_read_count):
        basic_stats = request.getfixturevalue(basic_stats_module)
        actual_read_count = summarize_read_count(basic_stats)

        assert actual_read_count.get("read_count") == expected_read_count


    def test_summarize_read_count_error_no_total_sequences(self):
        basic_stats = Module(
            name="Basic Statistics",
            status="pass",
            columns=["Measure", "Value"],
            data=[
                "Filename\tSRR1067505_1.fastq.gz",
                "File type\tConventional base calls",
                "Encoding\tSanger / Illumina 1.9",
                "Sequences flagged as poor quality\t0",
                "Sequence length\t36",
                "%GC\t47",
            ]
        )
        with pytest.raises(ValueError, match="Read count not found in 'Basic Statistics' module."):
            summarize_read_count(basic_stats)


class TestSummarizeBaseCount:
    @pytest.mark.parametrize("seq_len_dist_module, expected_base_count", [
        ("seq_len_dist_empty", 0),
        ("seq_len_dist_sra_data", 661023936),
        ("seq_len_dist_ngs_test", 3776539),
    ])
    def test_summarize_base_count_succeeds_well_formed_data(self, request, seq_len_dist_module, expected_base_count):
        seq_len_dist = request.getfixturevalue(seq_len_dist_module)
        actual_base_count = summarize_base_count(seq_len_dist)

        assert actual_base_count.get("base_count") == expected_base_count


@pytest.fixture
def basic_stats_empty() -> Module:
    """Basic Statistics module from FastQC file from empty FASTQ."""

    basic_stats = Module(
        name="Basic Statistics",
        status="pass",
        columns=["Measure", "Value"],
        data=[
            "Filename\tempty.fastq.gz",
            "File type\tnull",
            "Encoding Illumina\t1.5",
            "Total Sequences\t0",
            "Total Bases\t0 bp",
            "Sequences as poor quality\t0",
            "Sequence length\t0",
            "%GC\t0",
        ]
    )

    return basic_stats



@pytest.fixture
def basic_stats_sra_data() -> Module:
    """Basic Statistics module from FastQC file from SRR1067505."""

    basic_stats = Module(
        name="Basic Statistics",
        status="pass",
        columns=["Measure", "Value"],
        data=[
            "Filename\tSRR1067505_1.fastq.gz",
            "File type\tConventional base calls",
            "Encoding\tSanger / Illumina 1.9",
            "Total Sequences\t18361776",
            "Sequences flagged as poor quality\t0",
            "Sequence length\t36",
            "%GC\t47",
        ]
    )

    return basic_stats


@pytest.fixture
def basic_stats_ngs_test() -> Module:
    """Basic Statistics module from FastQC file in ngs-test repo."""

    basic_stats = Module(
        name="Basic Statistics",
        status="pass",
        columns=["Measure", "Value"],
        data=[
            "Filename\tSRR6924569_L001_raw_R1.fastq.gz",
            "File type\tConventional base calls",
            "Encoding\tSanger / Illumina 1.9",
            "Total Sequences\t50000",
            "Total Bases\t3.7 Mbp",
            "Sequences flagged as poor quality\t0",
            "Sequence length\t35-76",
            "%GC\t41",
        ]
    )

    return basic_stats


@pytest.fixture
def seq_len_dist_empty() -> Module:
    """Sequence Lengh Distribution module from FastQC file from empty FASTQ."""

    seq_len_dist = Module(
        name="Sequence Length Distribution",
        status="warn",
        columns=["Length", "Count"],
        data=[]
    )

    return seq_len_dist


@pytest.fixture
def seq_len_dist_sra_data() -> Module:
    """Sequence Lengh Distribution module from FastQC file from SRR1067505."""

    seq_len_dist = Module(
        name="Sequence Length Distribution",
        status="warn",
        columns=["Length", "Count"],
        data=[
            "36\t1.8361776E7",
        ]
    )

    return seq_len_dist


@pytest.fixture
def seq_len_dist_ngs_test() -> Module:
    """Sequence Lengh Distribution module from FastQC file in ngs-test repo."""

    seq_len_dist = Module(
        name="Sequence Length Distribution",
        status="warn",
        columns=["Length", "Count"],
        data=[
            "35\t1.0",
            "36\t0.0",
            "37\t1.0",
            "38\t0.0",
            "39\t0.0",
            "40\t1.0",
            "41\t0.0",
            "42\t0.0",
            "43\t0.0",
            "44\t0.0",
            "45\t0.0",
            "46\t0.0",
            "47\t1.0",
            "48\t0.0",
            "49\t0.0",
            "50\t1.0",
            "51\t1.0",
            "52\t0.0",
            "53\t3.0",
            "54\t0.0",
            "55\t0.0",
            "56\t0.0",
            "57\t1.0",
            "58\t2.0",
            "59\t0.0",
            "60\t1.0",
            "61\t1.0",
            "62\t0.0",
            "63\t2.0",
            "64\t3.0",
            "65\t3.0",
            "66\t4.0",
            "67\t4.0",
            "68\t1.0",
            "69\t3.0",
            "70\t14.0",
            "71\t41.0",
            "72\t242.0",
            "73\t868.0",
            "74\t2847.0",
            "75\t13355.0",
            "76\t32599.0",
        ]
    )

    return seq_len_dist
