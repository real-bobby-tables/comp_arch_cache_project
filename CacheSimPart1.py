import sys
import math
import argparse

parser = argparse.ArgumentParser(description="Cache Simulator - CS 3853 Spring 2021 - Group 6")

parser.add_argument('-s', '--CacheSize',
    dest='CacheSize',
    metavar='Cache Size',
    type=int,
    help="The size of the cache in kilobytes",
    required=True) #from 1KB to 1MB

parser.add_argument('-b', '--BlockSize',
    dest='BlockSize',
    metavar='Block Size',
    type=int,
    help="The size of the block in the cache",
    required=True) # 4 bytes to 64 bytes

parser.add_argument('-f', '--FileTrace',
    dest='FileTrace',
    metavar='Trace file',
    type=str,
    help="The name of the text file containing a trace",
    required=True)

parser.add_argument('-a', '--Associativity',
    dest='Associativity',
    metavar='Associativity',
    type=int,
    help="The associativity of the cache",
    required=True) # 1,2,4,8,16

parser.add_argument('-r', '--Replacement',
    dest='Replacement',
    metavar='Replacement policy',
    type=str,
    help="The replacement policy of this cache",
    required=True) # RR, RND, or LRU


args = parser.parse_args()


repDict = {'RR':"Round Robin", 'RND':"Random", 'LRU':"Least Recently Used"}
dataBus = 32

if args.Replacement not in repDict:
    print("Bad replacement, please use either RR, RND, or LRU")
    exit(1)



#check file
#filetxt = open(args.FileTrace)
#check CS
#check BS
#check RP

print("Cache Simulator - CS 3853 Spring 2021 - Group XX\n")

print("Trace File: ", args.FileTrace,"\n")

print("***** Cache Input Parameters *****")
print("Cache Size:\t\t\t\t\t",args.CacheSize,"KB")
print("Block Size:\t\t\t\t\t",args.BlockSize,"bytes")
print("Associativity Size:\t\t\t",args.Associativity)
print("Replacement Policy:\t\t\t",repDict[args.Replacement])

cSize = args.CacheSize
cSizeBytes = pow(2, (math.log(cSize, 2)+10))
bSize = args.BlockSize
aSoc = args.Associativity
ZEROES = '00000000'

class CacheBlock:
    def __init__self(self, size):
        self.num_entries = 0
        self.maxSize = size
        self.entries = {}

    def get_val(self, addr):
        return self.entries[addr]

    def set_val(self, addr, val):
        if self.num_entries < self.maxSize:
            self.entries[addr] = val
            self.num_entries = self.num_entries + 1
        else:
            print("Block is full!")

    def replace(self, addr, value):
        if self.entries.has_key(addr):
            self.entries[addr] = val




class Cache:
    def __init__(self, associativity, size, blockSize, rep_policy):
        self.associativity = associativity
        self.size = size
        self.blockSize = blockSize
        self.blocks = [CacheBlock(self.blockSize) for x in range(self.associativity)]
        self.rep_policy = rep_policy


def calculate_cache_values():

    blocks = cSizeBytes / bSize
    indB = math.log(cSizeBytes / (bSize * aSoc), 2)
    tagB = dataBus - indB - math.log(bSize, 2)
    rows = cSizeBytes / (bSize * aSoc)
    overhead = (blocks * 1 + blocks * tagB) / 8
    totalBytes = cSizeBytes + overhead
    impSize = (cSizeBytes + overhead) / 1024
    impSizeRU = math.ceil((cSizeBytes + overhead) / 1024)
    cost = round(impSizeRU * 0.09, 2)

    print("\n***** Cache Calculated Values *****\n")

    print("Total # Blocks:\t\t\t\t",blocks)
    print("Tag Size:\t\t\t\t\t",tagB,"bits")
    print("Index Size:\t\t\t\t\t",indB,"bits")
    print("Total # Rows:\t\t\t\t",rows)
    print("Overhead Size:\t\t\t\t",overhead,"bytes")
    print("Implementation Memory Size:\t",impSize,"KB","(",totalBytes,"bytes",")")
    print("Cost:\t\t\t\t\t\t $"+str(cost))

def parse_instruction_line(line):
    instr_arr = line.split()
    instr_len = instr_arr[1]
    instr_len_num = instr_len[1:3]
    instr_addr = instr_arr[2]
    print(f'Address: 0x{instr_addr}, length = {instr_len_num}')
    #print(instr_arr)
    return None

def parse_data_line(line):
    data_arr = line.split()
    src_tup = (data_arr[1], data_arr[2])
    dst_tup = (data_arr[4], data_arr[5])
    if (src_tup[0] == ZEROES and dst_tup[0] == ZEROES):
        print("No reads/writes occured")
        return None
    print(f'Data read at 0x{src_tup[0]}{src_tup[1]}, length=4')
    print(f'Data write at 0x{dst_tup[0]}{dst_tup[1]}, length=4')
    return None

def read_trace(tr):
    trace = []
    with open(tr, "r") as f:
        for line in f:
            trace.append(line.strip())
    return trace

def step(tr, instr_idx, data_idx):
    parse_instruction_line(tr[instr_idx])
    parse_data_line(tr[data_idx])


def simulate():
    print("\n\n\n***** Beginning Simulation ******")
    trace = read_trace(args.FileTrace)
    for i in range(0,len(trace),3):
        step(trace, i, i+1)





if __name__ == '__main__':
    calculate_cache_values()
    simulate()





'''
print("\n***** Trace File Contents *****\n")
i = 0
n = 0
for line in filetxt:
    if n == 20:
        break
    if i % 3 == 0:
        addr = line[5:7]
        leng = line[10:18]
        print("0x"+leng+ " ("+addr+")")
        n += 1
    i += 1
#'''