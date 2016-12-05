# cse180finalproject
CSE 180 Final Project:


1. Install BWA
2. Install FreeBayes
3. Install SAM tools

To run this program download from git and run:

python pipeline.py --input [input.fastq file] --reference [reference.fasta file]

You can specify the path to any of the tools above using the arguments
--bwa_path
--freebayes_path
--samtools_path

This program rates and scores the different snv desert segments of the input file based on a the number of snvs that occur, the length of the region the snvs occur in, and a synteny database created by the Sibelian tool. All output files are sent to the output folder and the final output table and key metrics are in output.txt. 
