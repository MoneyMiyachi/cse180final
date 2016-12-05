import os
import subprocess
import math
import numpy as np
import random
import matplotlib.pyplot as plt
import argparse
import time
import signal
import snvdeserts
import final_result


parser = argparse.ArgumentParser(description='Proccesses a .fasta File and returns the Unique SNP Deserts if they exist compared to Reference Genome.')
parser.add_argument('--input', metavar='I', type=str,
        help='a fasta file for the program to look for unique SNP Desert, Include the path.',
        required=True)
parser.add_argument('--output', metavar='O', type=str,
        help='final destination of the output file. Include the path.', required=False
        )
parser.add_argument('--bwa_path', required=False, default='bwa',
        help='path to bwa executable')
parser.add_argument('--freebayes_path', required=False, default='freebayes',
        help='path to freebayes executable')
parser.add_argument('--blast_path', required=False, default='blastn',
        help='path to blast executable')
parser.add_argument('--samtools_path', required=False, default='samtools',
        help='path to samtools executable')
parser.add_argument('--reference', required=True,
        help='a fasta reference file use for alignment, and variant calling')


args = parser.parse_args()
#print args
#subprocess.call(['ls', '-l'])
output = args.output
#print ", output
sam_file = open('./output/align.sam', 'w')

#indexing the reference file
index = subprocess.call([args.bwa_path, 'index', args.reference])

#aligning with bwaAligner
align =subprocess.Popen([args.bwa_path, 'mem', args.reference, args.input],
        stdout=sam_file)
sam_file.close()
align.wait()
#os.kill(align.pid,signal.SIG_IGN)


##convert to a bam
convert = subprocess.call([args.samtools_path, 'view', '-b','-o', './output/alignt.bam','./output/align.sam'])


#sort bam file
sort = subprocess.call([args.samtools_path, 'sort', '-T', '/tmp/temp.sorted', '-o', './output/align.sorted.bam', './output/align.bam'])


#indexing the sorted bam
index_bam = subprocess.call([args.samtools_path, 'index', './output/align.sorted.bam'])


#index the reference with samtools
re_index = subprocess.call([args.samtools_path, 'faidx', args.reference])


temp_vcf = open('./output/variants.vcf', 'w')
freebayes = subprocess.Popen([args.freebayes_path, '-f', args.reference, './output/align.sorted.bam'],
        stdout=temp_vcf)
freebayes.wait()
temp_vcf.close()

temp_vcf = './output/variants.vcf'

length = snvdeserts.ref_length(args.reference)
new_list = snvdeserts.extract_vcf(temp_vcf)
snv_table = snvdeserts.snp_desert(new_list,length)
output_list = snvdeserts.print_output(snv_table)


"""** need to have the sytnedb.txt in your repository **"""

result = final_result.final_output('./output/snv_output.txt','syntenydb.txt')
sorted_result = snvdeserts.sort_final()

sorted_file = open('./output/sorted_result.txt','w')
for x in sorted_result:
    #line = ','.join(repr(e) for e in x)
    s = str(x)
    line = s[1:-1]
    sorted_file.write(line)
    sorted_file.write('\t')
sorted_file.close()






