### **Step 3: `Gaussian CDF Fitting for GC Content and Abundance Estimation`**

pipeline_abundance_GaussF_esti_loop.py

Introduction
This Python script is designed to analyze GC content distribution in sequence data and estimate the sequence abundance by fitting a cumulative distribution function (CDF) of a Gaussian to the GC content profile. It serves as a post-processing tool following k-mer counting, allowing researchers to derive meaningful biological insights based on the GC composition and k-mer abundance patterns.

Features<br>
Analyzes the GC content of sequences represented by k-mers.<br>
Performs fitting of a Gaussian CDF to the sum of normalized k-mer counts grouped by GC content percentage.<br>
Extracts gene and transcript information from the input CSV filenames.<br>
Produces structured output for quick assessment of fit success and estimated parameters.<br>
Offers flexibility through user-defined minimum thresholds for k-mer counts appropriate for fitting.

Example usage:
```
python pipeline_abundance_GaussF_esti_loop.py --threshold 5 --input /path/to/merge_data --output / path/to/merge_data/results_file.csv
```
Command-Line Arguments<br>
--input: The path to the input folder containing the k-mer CSV files where each file should have a filename format including gene and transcript IDs (e.g., GENE_ENST00001234567_kmers.csv) (required).<br>
--output: The full path and name of the output CSV file where the results will be saved (required).<br>
--threshold: The minimum number of k-mers required for performing fitting; the default value is 10 if not specified.<br>
Output The script will output a CSV file containing the following columns:
Gene_Name: This is the name of the gene that the k-mers are associated with, typically extracted from the filename of the input CSV file according to a predetermined naming convention.

Transcript_ID: The identifier for the specific transcript from which the k-mers were derived. Like the gene name, this is also extracted from the filename of the input CSV file.

Global_Frequency: The frequency of the k-mer's occurrence across all transcripts in the dataset. This gives an idea of how common a particular k-mer sequence is overall.

Present_in_Transcripts: An identifier indicating which transcripts include the k-mer. This can be a single transcript ID or a list of IDs, depending on k-mer representation in the data.

Mini_Shared_Length: The minimum shared length between the input k-mer sequence and any of the transcripts. This value provides insight into the minimum overlap a k-mer has with known transcripts.

Sum or Fitted A (Abundance) for Normalized Count: For each k-mer fitting, this field either contains the sum of the normalized k-mer counts (if curve fitting fails or is not applicable) or the value 'A' from the successfully fitted Gaussian cumulative distribution function, which represents the abundance of the k-mer after normalization for transcript length.

Sum or Fitted A (Abundance) for Count: Similar to the above field, but for the raw k-mer count data. It contains the sum total of the raw counts (if curve fitting fails or is not applicable) or the value 'A' from the fitted Gaussian cumulative distribution function, indicating the overall abundance of the k-mer before normalization.

Fixed Mean (xc): The mean (or center) of the k-mer distribution, denoted by 'xc', as estimated from the Gaussian CDF fitting process. It is fixed based on an initial fitting of the local frequency data and used for subsequent fittings. If fitting was not performed, this field will be 'N/A'.

Fixed Standard Deviation (w): The standard deviation of the k-mer distribution, denoted by 'w', as estimated from the Gaussian CDF fitting process. It describes the spread or dispersion of the distribution. Similar to the fixed mean, this value is determined from an initial fit and used consistently for subsequent data. If fitting was not performed or failed, this field will be 'N/A'.

Report: A text field containing messages about the status of the data processing and any curve fitting processes. It can include messages such as 'OK' to indicate successful processing, 'Insufficient Data' if there isn't enough data to perform the fitting, or a detailed error message if fitting failed.
