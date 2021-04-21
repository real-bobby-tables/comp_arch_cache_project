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




print("Cache Simulator - CS 3853 Spring 2021 - Group XX\n")

print("Trace File: ", args.FileTrace,"\n")

print("***** Cache Input Parameters *****")
print("Cache Size:\t\t\t\t\t",args.CacheSize,"KB")
print("Block Size:\t\t\t\t\t",args.BlockSize,"bytes")
print("Associativity Size:\t\t\t",args.Associativity)
print("Replacement Policy:\t\t\t",repDict[args.Replacement])


class Cache:
    def __init__(self, associativity, size, blockSize, rep_policy):
        self.associativity = associativity
        self.size = size
        self.blockSize = blockSize
        #self.blocks = [CacheBlock(self.blockSize) for x in range(self.associativity)] removing this for now
        self.rep_policy = rep_policy
        self.cache_table = []

    def create_cache(self): 
        self.rows, self.cols = (math.floor(self.size/(self.blockSize*self.associativity)), 3 * self.associativity) # row = size/(block*assoc)  col = valid tag data
        print("row: col:",self.rows, self.cols)
        self.cache_table = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            
            for j in range(self.cols):
                    if j%3 == 0:
                        self.cache_table[i][j] = 0 #set valid bits to 0 for cache read
                   
        
    


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

def parse_instruction_line(line): #so the data parsing happens here but there seperate, how to update cache
    instr_arr = line.split()
    instr_len = instr_arr[1]
    instr_len_num = instr_len[1:3]
    instr_addr = instr_arr[2]
    global CLK, miss, hits
    CLK +=1

    offset = int(math.log(bSize,2))
    offset = math.ceil(offset/4)

    index =  int(math.log(cSizeBytes / (bSize * aSoc), 2))
    index =  math.ceil(math.log(cSizeBytes / (bSize * aSoc), 2)/4)
   
    offset_char = instr_addr[-offset:]
    index_char = instr_addr[-(index+offset):-offset]
    tag_char = instr_addr[0:-(index+offset)]
    for i in range(aSoc):
        if(i%3 == 0):
            val_bit = i
            if(cache.cache_table[index][i] == 0): #miss needs to figure out the strategy 
                cache.cache_table[index][i] = 1
                cache.cache_table[index][i+1] = tag_char
                cache.cache_table[index][i+2] = "data" 
                miss = miss + 1
                print("miss")
                #TODO: replacement algorithms
            elif(cache.cache_table[index][i] == 1): #miss
                if(cache.cache_table[index][val_bit +1] != tag_char):
                    cache.cache_table[index][i+1] = tag_char
                    cache.cache_table[index][i+2] = "data" #TODO actually replace the data?
                    miss = miss + 1
                    print("miss")
                elif (cache.cache_table[index][val_bit +1] == tag_char): #hits
                    hits = hits + 1
                    print("hit")
    

    print(f'Address: 0x{instr_addr}, length = {instr_len_num}')

  
    return None

def parse_data_line(line):
    data_arr = line.split()
    src_tup = (data_arr[1], data_arr[2])
    dst_tup = (data_arr[4], data_arr[5])

    

    if (src_tup[0] == ZEROES and dst_tup[0] == ZEROES):
        print("No reads/writes occured")
        return None
    #print(f'Data read at 0x{src_tup[0]}{src_tup[1]}, length=4') #TODO: i think this is where the cache studd will happen. Maybe pass a function
    #print(f'Data write at 0x{dst_tup[0]}{dst_tup[1]}, length=4')
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

#global values
cSize = args.CacheSize
cSizeBytes = pow(2, (math.log(cSize, 2)+10))
bSize = args.BlockSize
aSoc = args.Associativity
ZEROES = '00000000'
#global cpi calculates
total = 0
hits = 0
miss = 0
conflict = 0
compuls =0
blocks = cSizeBytes / bSize
CLK =0
#Cache declorations
cache = Cache(aSoc,cSizeBytes,bSize,repDict[args.Replacement]) #TODO, update to the trace or step to take in cache as an argument
cache.create_cache()

if __name__ == '__main__':
    
    calculate_cache_values()
    simulate()
    print("", CLK, hits, miss)
