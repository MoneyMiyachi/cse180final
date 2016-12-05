def get_blocks(synteny_file, reference):
    blocks = {}
    reference_id = ''
    reference_number = ''
    with open(reference, 'r') as f2:
        line = f2.readline()
        parts = line.split()
        reference_id = parts[0][1:]
        print(reference_id)
    with open(synteny_file, 'r') as f:
        for line in f:
            parts = line.split()
            if parts[0][0] == '-':
                break
            if parts[2] == reference_id:
                reference_number = parts[0]
        print(reference_number)
        print(line)
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
    #print(blocks)
    return blocks

def block_parser(synteny_file, reference, blocks):
    out = open('syntenydb.txt', 'w')
    out.write('block number\tstart\tend\tnum blocks\n')
    reference_id = ''
    reference_number = ''
    with open(reference, 'r') as f2:
        line = f2.readline()
        parts = line.split()
        reference_id = parts[0][1:]
        print(reference_id)
    with open(synteny_file, 'r') as f:
        for line in f:
            parts = line.split()
            if parts[0][0] == '-':
                break
            if parts[2] == reference_id:
                reference_number = parts[0]
        print(reference_number)
        print(line)
        while line != '':
            line = f.readline()
            if line == '':
                break
            parts = line.split()
            if parts[0] == 'Block':
                block_number = parts[1][1:]
                line = f.readline()
                if block_number in blocks:
                    wanted_line = f.readline()
                    #print(wanted_line)
                    parts = wanted_line.split()
                    while(wanted_line.split()[0][0] != '-'):
                        #print(wanted_line[0])
                        #print(wanted_line[0] == reference_number)
                        if(wanted_line[0] == reference_number):
                            parter = wanted_line.split()
                            if int(parter[2]) > int(parter[3]):
                                out.write("%s\t%s\t%s\t%s\n" %(block_number, parter[2],parter[3], blocks[block_number]))
                            else:
                                out.write("%s\t%s\t%s\t%s\n" %(block_number,parter[3],parter[2], blocks[block_number]))
                        wanted_line = f.readline()
    out.close()


#wanted_blocks = get_blocks('blocks_coords.txt', 'reference2.fa.txt')
#block_parser('blocks_coords.txt', 'reference2.fa.txt', wanted_blocks)

