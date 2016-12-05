"""File that creates a usable synteny database for our tool to use. 
   Takes in input from Sibelia run on multiple references and outputs a
   text file that will be used as input for final_output.py
   Output is formatted as block number\tstart\tend\tnumber of species that have
   block"""


"""Function that takes in Sibelia text file and reference genome and outputs a
   only those blocks that are shared between reference and a different species"""
def get_blocks(synteny_file, reference):
    blocks = {} #output variable
    
	#will be needed to identify referene from synteny_file
	reference_id = ''
    reference_number = ''

	#identify reference accession number within reference
    with open(reference, 'r') as f2:
        line = f2.readline()
        parts = line.split()
        reference_id = parts[0][1:]
		
	#identify reference within synteny_file
    with open(synteny_file, 'r') as f:
        for line in f:
            parts = line.split()
            if parts[0][0] == '-':
                break
            if parts[2] == reference_id:
                reference_number = parts[0]
		#parse synteny file to get a list of blocks that are between species
        block_number = 0
        while line != '':
            line = f.readline()
            if line == '':
                break
            parts = line.split()
            if parts[0] == 'Block':
                block_number = parts[1][1:]
                line = f.readline()
                wanted_line = f.readline()
                parts = wanted_line.split()
                sequences = []
                while(wanted_line.split()[0][0] != '-'):
                    if(wanted_line[0] not in sequences):
                        sequences.append(wanted_line[0])
                    wanted_line = f.readline()
                if(len(sequences) > 1 and reference_number in sequences):
                    blocks[block_number] = len(sequences)
    return blocks

"""Function that takes in Sibelia synteny block file, reference and blocks that
   are in reference and other species and returns usable synteny databese for
   tool"""
def block_parser(synteny_file, reference, blocks):
    
	#Get sample_id for reference species
	out = open('syntenydb.txt', 'w')
    out.write('block number\tstart\tend\tnum blocks\n')
    reference_id = ''
    reference_number = ''
    with open(reference, 'r') as f2:
        line = f2.readline()
        parts = line.split()
        reference_id = parts[0][1:]
    
	#look for lines that include blocks in block parameter
	with open(synteny_file, 'r') as f:
        for line in f:
            parts = line.split()
            if parts[0][0] == '-':
                break
            if parts[2] == reference_id:
                reference_number = parts[0]
        while line != '':
            line = f.readline()
            if line == '':
                break
            parts = line.split()

			#if we find a good block
            if parts[0] == 'Block':
                block_number = parts[1][1:]
                line = f.readline()
                if block_number in blocks:
                    wanted_line = f.readline()
                    parts = wanted_line.split()
						
					#find the synteny regions and output their info
                    while(wanted_line.split()[0][0] != '-'):
                        if(wanted_line[0] == reference_number):
                            parter = wanted_line.split()
                            if int(parter[2]) > int(parter[3]):
                                out.write("%s\t%s\t%s\t%s\n" %(block_number, parter[2],parter[3], blocks[block_number]))
                            else:
                                out.write("%s\t%s\t%s\t%s\n" %(block_number,parter[3],parter[2], blocks[block_number]))
                        wanted_line = f.readline()
    out.close()
