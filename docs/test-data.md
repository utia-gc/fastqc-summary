# Test data

FastQC ZIP files were acquired from public sources or generated in order to test fastqc-summary.

## Fetch or produce FastQC ZIP files

Test data in the format of FastQC zip output files was obtained from the MultiQC test repo:

```bash
curl -L --create-dirs --output tests/data/SRR1067505_1_fastqc.zip https://github.com/MultiQC/test-data/raw/refs/heads/main/data/modules/fastqc/v0.11.2/SRR1067505_1_fastqc.zip
```

Test data for FASTQ files with no reads:

```bash
# create a gzipped fastq file with no reads
echo "" | gzip > tests/data/empty.fastq.gz

# run fastqc on the empty file
apptainer exec "https://depot.galaxyproject.org/singularity/fastqc%3A0.12.1--hdfd78af_0" fastqc tests/data/empty.fastq.gz

# delete everything except the zip file
rm tests/data/empty.fastq.gz tests/data/empty_fastqc.html
```
