# FastQC Summary

A utility for summarizing data from FastQC runs.

## Purpose

[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) produces a lot of valuable data.
Much of this data can be further mined, processed, and summarized to generate valuable information about sequencing results.

FastQC Summary mines, processes, and summarizes information from the ZIP file produced by FastQC and returns this information to the user as structured data.

> [!NOTE]
> While these summaries are reported on the FastQC data, they are primarily understood to be summaries about the FASTQ (or other sequencing format) file that was QC'ed by FastQC.

## Output

The output of FastQC Summary are summaries of FastQC data structured as a JSON object.

### Available summaries

The following summaries are available:

| Name | Key | Value type | Description |
| --- | --- | --- | --- |
| Read count | `read_count` | number | The count of reads (sequences). |
| Base count | `base_count` | number | The count bases in reads (sequences). |

## Installation

### Apptainer

The most convenient way to use FastQC Summary is through the official [Apptainer container image](https://github.com/utia-gc/fastqc-summary/pkgs/container/fastqc-summary) available publicly on the GitHub Container Registry:

```bash
apptainer pull oras://ghcr.io/utia-gc/fastqc-summary:v2.0.0
```

### uv

uv was used to develop FastQC Summary and is the easiest method for installing the CLI app.

Install FastQC Summary user-wide with the `uv tool install` interface:

```bash
uv tool install git+https://github.com/utia-gc/fastqc-summary@v2.0.0
```

Run FastQC Summary in a temporary environment managed by uv:

```bash
uvx git+https://github.com/utia-gc/fastqc-summary@v2.0.0
```

### pip

FastQC Summary can also be installed with pip.

FastQC Summary requires requires Python >= v3.13.
If a compatible Python version is not available, installation with pip will fail.
Note that uv is preferred because it will manage the Python version for you.

Install FastQC Summary into a clean virtual environment with pip:

```bash
# create fresh virtual environment
python3 -m venv .venv
# activate the virtual environment
. .venv/bin/activate
# install FastQC Summary into the virtual environment
python3 -m pip install git+https://github.com/utia-gc/fastqc-summary@v2.0.0
```

## Usage

The FastQC Summary CLI app is accessed with the `fastqc-summary` command.

If installed through the Apptainer image, access the command through `apptainer exec`:

```bash
apptainer exec oras://ghcr.io/utia-gc/fastqc-summary:v2.0.0 fastqc-summary
```

If installed with uvx, access through the `uvx` command:

```bash
uvx git+https://github.com/utia-gc/fastqc-summary@v2.0.0
```

Otherwise, if FastQC Summary is available on your path, e.g. by installing with `uv tool install` or `pip` inside an active virtual environment, access the command directly:

```bash
fastqc-summary
```

The usage docs here use this method for simplicity.

> [!CAUTION]  
> See [Installation section above](#installation) for comments on versioning.

### Requirements and sample data

FastQC Summary requires a ZIP archive of FastQC data.
This is simply the .zip file that is a default output of FastQC.

See the [test data docs](/docs/test-data.md#fetch-or-produce-fastqc-zip-files) for instructions on how to download an example FastQC ZIP archive.
This usage section will assume that you have this FastQC ZIP archive available at the path `SRR1067505_1_fastqc.zip`.

### Usage help

Basic usage and help messages can be printed to the terminal by providing no arguments or the `-h` or `--help flags`:

```bash
# print basic usage
fastqc-summary

# print help message
fastqc-summary -h
fastqc-summary --help
```

### Basic usage

The most basic usage of FastQC Summary takes a single FastQC ZIP archive as a positional argument.
The summaries are represented as a JSON object which is sent to stdout and therefore printed to the console.

```bash
fastqc-summary SRR1067505_1_fastqc.zip
```

As with any stdout, you can redirect the output to a file, pipe it into another process, etc:

```bash
# redirect summary output to file
fastqc-summary SRR1067505_1_fastqc.zip > SRR1067505_1_fastqc-summary.json
```

#### Control output

`fastqc-summary` provides the `-o`/`--output` command-line flag to write the JSON object of summaries to a file.

The following commands are equivalent to each other and write the same file as the redirected stdout above:

```bash
fastqc-summary SRR1067505_1_fastqc.zip -o SRR1067505_1_fastqc-summary.json
fastqc-summary SRR1067505_1_fastqc.zip --output SRR1067505_1_fastqc-summary.json
```
