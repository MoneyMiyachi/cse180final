import numpy
import math
import random
import operator
import argparse

"""
parser = argparse.ArgumentParser(description='Processes a reference file and a vcf file and creates a table with metrics scoring the quality of different snp deserts')

parser.add_argument('-r', '--reference', required=True,
        help='a fasta reference file use for alignment, and variant calling')

parser.add_argument('-v', '--vcf', required=True,
        help='a vcf file use for alignment, and variant calling')
"""
def ref_length(reference):
    chars = 0
    with open(reference, 'r') as in_file:
        next(in_file)
        for line in in_file:
            s_line = line.rstrip('\n')
            chars += len(s_line)
        return chars

def extract_vcf(vcf_file):
    with open(vcf_file,'r') as f:
        pos_list = set()
        for line in f:
            parts = line.split()
            if parts[0][0] != '#':
                parts = line.split()
                pos_list.add(parts[1])
    return pos_list

def snp_desert(pos_list, length):
    desert_dict = {}
    f_dict = {}
    for i in range(1,length+1):
        if str(i) in pos_list:
            f_dict[i] = [1,i,i]
        else:
            f_dict[i] = [0,i,i]
    #iters = int(math.log(length,2))
    #print iters
    combos = f_dict.values()
    count = [item[0] for item in combos]
    for increment in range(50,5050,50):
        for i in range(increment,length,increment):
            rating = sum(count[i-increment:i])
            #print rating
            desert_dict[i-increment,i] = [rating, i-increment, i]
        #print x
    sorted_desert = sorted(desert_dict.items(), key=lambda k: k[1][0], reverse=True)
    return sorted_desert


def print_output(top_snps):
    target = open('./output/snv_output.txt','w')
    target.write("start end length  snps conservation score")
    target.write("\n")
    snp_output = []
    for i in range(len(top_snps)):
        start = top_snps[i][0][0]
        end = top_snps[i][0][1]
        length = end - start
        snps = top_snps[i][1][0]
        conservation_score = length/(snps+1)
        snp_output.append([start,end,length,snps,conservation_score])
        #print ','.join(str(snp_output[0]))
    snp_output.sort(key=lambda x: x[4], reverse=True)
    for i in range(len(snp_output)):
        start = snp_output[i][0]
        end = snp_output[i][1]
        length = snp_output[i][2]
        snps = snp_output[i][3]
        conservation_score = snp_output[i][4]
        #print "THIS SHOULD BE FUCKING WRITING"
        target.write(str(start))
        target.write('\t')
        target.write(str(end))
        target.write('\t')
        target.write(str(length))
        target.write('\t')
        target.write(str(snps))
        target.write('\t')
        target.write(str(conservation_score))
        target.write("\n")
    target.close()







"""
def sort_final():
    with open('output.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('final_sort.txt', 'w') as fout:
        fout.writelines(data[1:len(data)/2])
    fin.close()
    fout.close()
    final_matrix = numpy.loadtxt('final_sort.txt')
    col = 7
    final_matrix[numpy.array(final_matrix[:,col].argsort(axis=0).tolist()).ravel()]
    final_matrix[:] == final_matrix[::-1]
    return final_matrix


def position_sort():
    with open('output.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('position_sort.txt', 'w') as fout:
        fout.writelines(data[1:])
    fin.close()
    fout.close()
    pos_sort = numpy.loadtxt('position_sort.txt')
    col = 0
    final_matrix[numpy.array(final_matrix[:,col].argsort(axis=0).tolist()).ravel()]
    final_matrix[:] == final_matrix[::-1]

#args = parser.parse_args()

length = ref_length('small_test/small_test_ref.fa')
new_list = extract_vcf('temp.vcf')
snp_table = snp_desert(new_list,length)
#print length
#new_list = extract_vcf(args.vcf)
#print new_list
#snp_table = snp_desert(new_list,length)
#print snp_table
#rando_list = print_output(snp_table)"""


