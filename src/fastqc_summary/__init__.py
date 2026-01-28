import json
import sys

from fastqc_summary.cli import get_args
from fastqc_summary.parser import (
    Module,
    parse_modules,
)
from fastqc_summary.summaries import (
    summarize_base_count,
    summarize_read_count,
)

def main() -> None:
    """FastQC summary application logic.

    `main()` serves as the entrypoint for the FastQC summary CLI application.
    It parses and validates command-line arguments, computes summaries on FastQC data, and writes those summaries.

    `main()` takes no argument and returns no values.
    """

    args = get_args()

    # map the modules needed to compute the summaries to an in memory representation of the modules
    modules = dict.fromkeys(("Basic Statistics", "Sequence Length Distribution"), None)
    for module in parse_modules(args.fastqc_archive):
        if module.name in modules.keys():
            modules[module.name] = module

    # compute the summaries
    summaries = {}
    summaries.update(summarize_read_count(modules["Basic Statistics"]))
    summaries.update(summarize_base_count(modules["Sequence Length Distribution"]))

    if isinstance(args.output, str):
        with open(args.output, "w") as output_json:
            json.dump(summaries, output_json)
    elif args.output == sys.stdout:
        json.dump(summaries, args.output)
