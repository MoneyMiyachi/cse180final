"""File that contains function for combining synteny and snvdesert regions into
   output file in pipeline."""

import numpy
import math
import random
import operator
import argparse

"""Function that takes in a snvdesert file and a synteny database and outputs a
   file that combines the information of the two into human readable format"""
def final_output(SNP_deserts, syntenydb):
    f1 = open(SNP_deserts, 'r')
    f3 = open('./output/output.txt', 'w')
    header = f1.readline()
    header = header.rstrip('\n')
    f3.write(header + "\tpercent_synteny\tblocks\tspecificity_score\n")

	#read each snvdesert region from file
    for line1 in f1:
        parts = line1.split()
        #print(parts)
        start_SNP = int(parts[0])
        end_SNP = int(parts[1])
        length = int(parts[2])
        f2 = open(syntenydb, 'r')
        f2.readline()
		#for each snvdesert region, check to see how much of it if any is in a
		#synteny block
        for line2 in f2:
            output = []
            parts2 = line2.split()
            start_synteny = int(parts2[1])
            end_synteny = int(parts2[2])
            num_synteny = int(parts2[3])
            in_synteny_block = False

			#if any part is in synteny
            if(start_SNP >= start_synteny and start_SNP <= end_synteny) or (end_SNP >= start_synteny and end_SNP <= end_synteny):
                
				#if whole thing is in synteny
				if(start_SNP >= start_synteny and end_SNP <= end_synteny):
                    output.append('1.00')
                    output.append(num_synteny)
                    f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), output[0], output[1], str(float(output[0])*int(output[1]))))
                    in_synteny_block = True
                    break

				#if last part is in synteny
                elif start_SNP <= start_synteny and end_SNP <= end_synteny:
                    in_synteny = float(end_SNP - start_synteny)/length
                    output.append(str(in_synteny))
                    output.append(num_synteny)
                    f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), output[0], output[1], str(float(output[0])*int(output[1]))))
                    in_synteny_block = True
                    break

				#if first part is in synteny
                elif(start_SNP >= start_synteny and end_SNP >= end_synteny):
                    in_synteny = float(end_SNP-end_synteny)/length
                    output.append(str(in_synteny))
                    output.append(num_synteny)
                    f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), output[0], output[1], str(float(output[0])*int(output[1]))))
                    in_synteny_block = True
                    break
            else:
                continue

        if not in_synteny_block:
            f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), '0', num_synteny, '0'))
        f2.close()
    f1.close()
    f3.close()


