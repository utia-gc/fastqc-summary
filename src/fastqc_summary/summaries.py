"""Summary functions for FastQC modules.

The summary functions take a representation of the apropriate FastQC module data
and return a useful summary of that data.

Typical usage example:
"""

from decimal import Decimal

from fastqc_summary.parser import Module


def summarize_read_count(basic_stats: Module) -> dict[str, int]:
    """Extract the total count of reads from basic statistics module."""

    read_count = None
    # extract read count from total sequences line
    for line in basic_stats.data:
        if line.startswith("Total Sequences"):
            read_count = line.split("\t")[1]
            break

    # basic stats module must contain read counts
    if not read_count:
        raise ValueError("Read count not found in 'Basic Statistics' module.")

    return {"read_count": int(read_count)}


def summarize_base_count(seq_len_dist: Module) -> dict[str, int]:
    """Compute the total count of bases from sequence length distribution module."""

    base_count = 0

    # compute total count of bases
    # the total count of bases in a file of sequence reads can be computed from a frequency table of sequence lengths
    # that is, base_count = <length, count>, where <length, count> is the dot product of the two n-vectors length and count,
    # length_i is the number of bases in the ith element, and
    # count_i is the count of reads with the corresponding length
    for line in seq_len_dist.data:
        length_i, count_i = line.split("\t")
        # handle conversion of counts with trailing ".0" or scientific notation to integer
        count_i = int(Decimal(count_i))
        base_count += int(length_i) * count_i

    return {"base_count": base_count}
