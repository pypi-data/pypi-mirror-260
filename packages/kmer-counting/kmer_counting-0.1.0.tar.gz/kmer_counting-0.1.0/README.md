kmer_counting_loop.py

Introduction
This tool is designed for bioinformatics analysis to count k-mer frequencies in sequencing data stored in FASTQ format. It is particularly useful when dealing with large datasets as it leverages Python's multiprocessing capabilities for parallel processing, thus enhancing performance and reducing computation time.
Features
Count specified k-mer sizes in FASTQ files (compressed with gzip).<br>
Use input CSV files containing k-mer sequences to filter and count only relevant k-mers.<br>
Handle large datasets efficiently with chunk-based parallel processing.<br>
Utilize multiple CPU cores for faster computation.<br>
Generate output CSV files containing the count of each k-mer.<br>