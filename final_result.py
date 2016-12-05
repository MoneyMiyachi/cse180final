import numpy
import math
import random
import operator
import argparse


def final_output(SNP_deserts, syntenydb):
    f1 = open(SNP_deserts, 'r')
    f3 = open('./output/output.txt', 'w')
    header = f1.readline()
    header = header.rstrip('\n')
    f3.write(header + "\tpercent_synteny\tblocks\tspecificity_score\n")

    for line1 in f1:
        parts = line1.split()
        #print(parts)
        start_SNP = int(parts[0])
        end_SNP = int(parts[1])
        length = int(parts[2])
        f2 = open(syntenydb, 'r')
        f2.readline()
        for line2 in f2:
            output = []
            parts2 = line2.split()
            start_synteny = int(parts2[1])
            end_synteny = int(parts2[2])
            num_synteny = int(parts2[3])
            #print(parts2)
            in_synteny_block = False


            if(start_SNP >= start_synteny and start_SNP <= end_synteny) or (end_SNP >= start_synteny and end_SNP <= end_synteny):
                if(start_SNP >= start_synteny and end_SNP <= end_synteny):
                    output.append('1.00')
                    output.append(num_synteny)
                    #print "BLOCK1", (output), line1.rstrip('\n'), start_synteny, end_synteny, length

                    f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), output[0], output[1], str(float(output[0])*int(output[1]))))
                    in_synteny_block = True
                    break


                elif start_SNP <= start_synteny and end_SNP <= end_synteny:
                    in_synteny = float(end_SNP - start_synteny)/length
                    output.append(str(in_synteny))
                    output.append(num_synteny)
                    #print "BLOCK 2", (output), line1.rstrip('\n'), start_synteny, end_synteny, length, float(end_SNP-start_synteny)
                    f3.write("%s\t%s\t%s\t%s\n" % (line1.rstrip('\n'), output[0], output[1], str(float(output[0])*int(output[1]))))
                    in_synteny_block = True
                    break


                elif(start_SNP >= start_synteny and end_SNP >= end_synteny):
                    in_synteny = float(end_SNP-end_synteny)/length
                    output.append(str(in_synteny))
                    output.append(num_synteny)
                    #print "BLOCK3", (output), line1.rstrip('\n'), start_synteny, end_synteny, length, float(end_SNP-end_synteny)
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


#output('SNP_desert.txt','syntenydb.txt')
