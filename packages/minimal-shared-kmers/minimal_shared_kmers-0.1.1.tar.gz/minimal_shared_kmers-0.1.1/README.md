### **Step 1: `minimal-shared region filtering`**

kmer_frequency_distribution_mini_shared.py 

This tool processes a FASTA file containing transcript sequences and outputs a set of CSV files that summarize the k-mer content for each transcript. Each CSV file contains a list of k-mers of specified length that are present in the transcript, along with their local and global frequency, and information on which transcripts each k-mer is present in.

Features
K-mer Counting: For a given transcriptome FASTA file, count all k-mers of a specified length (default is set to 50).<br>
Minimal Shared K-mers Output: For each transcript, output the k-mers that have the minimum global frequency—the smallest number of transcripts in which the k-mer appears.<br>
CSV Output Content: Generate a CSV file for each isoform with the following columns:<br>

'kmer': The k-mer sequence.<br>
'Local_Frequency': The number of times the k-mer appears in the specific isoform.<br>
'Global_Frequency': The number of transcripts that contain the k-mer across the entire transcriptome.<br>
'Present_in_Transcripts': A list of transcript identifiers that share the k-mer if its global frequency is more than 1. For unique k-mers, the identifier of the single transcript is given.

Installation

To install the specific version (0.1.0) of the package `minimal-shared-kmers` using pip, run the following command in your terminal:

```bash
pip install minimal-shared-kmers==0.1.0
```
Usage
To use this tool, you need to have Python installed on your system. The script requires a FASTA file with the transcript sequences as input and a directory path where the CSV files will be saved as output.

Execute the script with the necessary arguments from the command line. For example:<br>
```python
python kmer_frequency_distribution_mini_shared.py --input path/to/your/ACTB_reference/mart_export_ACTB.txt --output path/to/output/directory/
```
Command-Line Arguments<br>
--input: Path to the input FASTA file containing transcript sequences (https://useast.ensembl.org/biomart/martview/aeb3390f02325ab7951be9a7d6daaa42).<br> 
--output: Path to the output directory where CSV files for each transcript will be saved.

Output File Details
For each transcript in the input FASTA file, the script will create a corresponding CSV file in the output directory with a name derived from the transcript header, sanitized to be filesystem-friendly.

In the output CSV files for each transcript, only k-mers that have the smallest global frequency for that transcript are included. If multiple k-mers share the same smallest global frequency, then all such k-mers are included in the CSV file. The 'Present_in_Transcripts' field in the CSV may include multiple transcript names, indicating that those transcripts share the k-mer.

If the global frequency of a k-mer is 1, indicating that it is unique to a single transcript, then the 'Present_in_Transcripts' field will only contain the identifier of that specific transcript.
