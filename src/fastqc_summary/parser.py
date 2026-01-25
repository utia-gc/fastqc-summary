"""Parse the FastQC data.

FastQC data is in a semistructured format in a file inside of a FastQC ZIP archive file.
The FastQC data must be read from the fastqc_data.txt file and parsed module by module to be useful.

Typical usage examples:
"""

from dataclasses import dataclass
import io
from typing import Iterator
import zipfile


@dataclass
class Module:
    """Representation of a module of FastQC data.

    Attributes:
        name: A name for the module.
        status: A status for the module, one of [pass, warn, fail].
        columns: Column names for the data fields.
        data: Rows of data for the module.
    """
    name: str
    status: str
    columns: list[str]
    data: list[str]


def parse_modules(zip_path: str) -> Iterator[Module]:
    """Read and parse modules from fastqc_data.txt file in a ZIP archive.

    Args:
        zip_path: Path to a ZIP archive file.

    Yields:
        A representation of a module from fastqc_data.txt.
    """
    with (
        zipfile.ZipFile(zip_path, "r") as archive,
        archive.open(find_fastqc_data_file(archive), "r") as fastqc_data_bytes,
        io.TextIOWrapper(fastqc_data_bytes, encoding="utf-8") as fastqc_data_text,
    ):
        # initialize with an empty Module
        module = Module(name="", status="", columns=[], data = [])

        for line in fastqc_data_text:
            line = line.rstrip()

            # yield current module if end of module reached and module isn't empty
            if line.startswith(">>END_MODULE") and module.name:
                yield module

            # start new module
            elif line.startswith(">>") and not line.endswith("END_MODULE"):
                module = Module(name=line.split("\t")[0][2:], status=line.split("\t")[1], columns=[], data = [])

            # add module column names
            elif line.startswith("#") and module.name:
                module.columns = line[1:].split("\t")

            # add data rows to module
            elif module.name:
                module.data.append(line)


def find_fastqc_data_file(archive: zipfile.ZipFile) -> str:
    candidates = [file for file in archive.namelist() if file.endswith("fastqc_data.txt")]

    if not candidates:
        raise FileNotFoundError("fastqc_data.txt not found in archive")
    if len(candidates) > 1:
        raise ValueError(f"Multiple fastqc_data.txt files found in archive: {candidates}")

    return candidates[0]
