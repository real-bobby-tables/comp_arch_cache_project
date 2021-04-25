import sys
import math
import argparse
import random

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

def calculate_cpi_calues():

    hit_rate = (hits * 100)/total
    miss_rate = 1 - hit_rate
    blocks = cSizeBytes / bSize
    indB = math.log(cSizeBytes / (bSize * aSoc), 2)
    tagB = dataBus - indB - math.log(bSize, 2)
    overhead = (blocks * 1 + blocks * tagB) / 8
    impSize = (cSizeBytes + overhead) / 1024
    impSizeRU = math.ceil((cSizeBytes + overhead) / 1024)
    cost = round(impSizeRU * 0.09, 2)
    unused_blocks = ((blocks - compuls)* (bSize + overhead))/1024
    waste = cost * unused_blocks #kb?
    #CPI = Number Cycles/Number Instruction needs to get count

  
    print("\n***** CACHE SIMULATION RESULTS *****\n")
    print("Total Cache Accesses:\t\t",total)
    print("Cache Hits:\t\t\t",hits)
    print("Cache Misses:\t\t\t",miss)
    print("--- Compulsory Misses:\t\t",compuls)
    print("--- Conflict Misses:\t\t",conflict)

    print("\n*****  CACHE HIT & MISS RATE: *****\n")

    print("Hit Rate:\t\t\t",hit_rate) #// (Hits * 100) / Total Accesses
    print("Miss Rate:\t\t\t",miss_rate)   #1 – Hit Rate           
    print("CPI:14.14 Cycles/Instruction  (7)", num_cycles)  #// Number Cycles/Number Instructions 
    # // Unused KB = ( (TotalBlocks-Compulsory Misses) * (BlockSize+OverheadSize) ) / 1024
    #// The 1024 KB below is the total cache size for this example
    #// Waste = COST/KB * Unused KB               
    print("Unused Cache Space:\t\t",(blocks - compuls),"Kb","/",(bSize+overhead) ,"Kb" ,"=", unused_blocks, "Waste: $", waste)
    print("Unused Cache Blocks:\t\t", unused_blocks, "/",blocks)  


def update_block(Replacement,index,val_bit,tag):
     global miss, hits,conflict,compuls,num_cycles
     #print(Replacement)
     isnt_full =-1
     for i in range(cache.cols):
         #so its just going through the range like 1 =0 3 = 3 and not the array index
         if(i%3 == 0):
            
            if(cache.cache_table[index][i] == 0): 
                isnt_full = i

     if(cache.cache_table[index][val_bit] == 0):

        cache.cache_table[index][val_bit] = 1
        cache.cache_table[index][val_bit+1] = tag
        cache.cache_table[index][val_bit+2] = CLK 
        print("miss 165")
        miss = miss + 1
        compuls += 1
        return None

     elif(isnt_full >= 0):
        
        cache.cache_table[index][isnt_full+1] = tag
        cache.cache_table[index][isnt_full+2] = CLK  
        print("miss 174")
        miss = miss + 1
        compuls += 1
        return None

     elif(cache.cache_table[index][val_bit] == 1 ):
        if(Replacement == 'Least Recently Used'):
            #print("lru")
            lru = cache.cache_table[index][val_bit+2] 
            victim_index = 0
            for i in range(cache.cols):
                if(i%3 ==0):
                    if lru < cache.cache_table[index][i+2]:
                        victim_index = i
                        lru = cache.cache_table[index][i+2]
            cache.cache_table[index][victim_index + 1] = tag
            cache.cache_table[index][victim_index + 2] = CLK
            miss = miss + 1
            print("miss 192")
            conflict = conflict +1
            return None

        elif(Replacement != 'Least Recently Used'):
            #print("random")
            random_bit = random.randint(0,aSoc-1)*3 
                    
            cache.cache_table[index][random_bit + 1] = tag
            cache.cache_table[index][random_bit + 2] = CLK 
            miss = miss + 1
            conflict = conflict +1
            return None

def cache_parse(line):

    global CLK, miss, hits, total,num_cycles

    CLK +=1
    total +=1

    offset = int(math.log(bSize,2)) 
    offset = math.ceil(offset/4)

    index =  int(math.log(cSizeBytes / (bSize * aSoc), 2))
    index = math.floor(index/4) #TODO: check this but it works
    
   
    offset_char = line[-offset:]
    index_char = line[-(index+offset):-offset]
    tag_char = line[0:-(index+offset)]

    index = int(index_char,16)
    
    for i in range(cache.cols):
        if(i%3 == 0):
            val_bit = i
            if(cache.cache_table[index][i] == 0):  
                update_block(cache.rep_policy,index,val_bit,tag_char)
                return None
                
            elif(cache.cache_table[index][i] == 1): 

                if(cache.cache_table[index][val_bit +1] != tag_char):
                    update_block(cache.rep_policy,index,val_bit,tag_char)
                    return None

                elif (cache.cache_table[index][val_bit +1] == tag_char): #hits
                    
                    hits = hits + 1
                    num_cycles +=1
                    return None

def parse_instruction_line(line): #so the data parsing happens here but there seperate, how to update cache
    global num_cycles
    instr_arr = line.split()
    instr_len = instr_arr[1]
    instr_len_num = instr_len[1:3]
    instr_addr = instr_arr[2]

    num_cycles +=2
    cache_parse(instr_addr)
                    
    

    #print(f'Address: 0x{instr_addr}, length = {instr_len_num}')

  
    return None

def parse_data_line(line):
    global num_cycles
    data_arr = line.split()
    src_tup = (data_arr[1], data_arr[2])
    dst_tup = (data_arr[4], data_arr[5])

    
    if (src_tup[0] == ZEROES and dst_tup[0] == ZEROES):
        
        return None
        
    elif(src_tup[0] != ZEROES and dst_tup[0] != ZEROES):
        
        cache_parse(data_arr[1])
        cache_parse(data_arr[5])
        num_cycles +=2
        
    elif (src_tup[0] != ZEROES and dst_tup[0] == ZEROES):
        cache_parse(data_arr[1])
        num_cycles +=1
        
    elif (src_tup[0] == ZEROES and dst_tup[0] != ZEROES):
        cache_parse(data_arr[5])
        num_cycles +=1
        
    #print(f'Data read at 0x{src_tup[0]}{src_tup[1]}, length=4') 
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
num_cycles =0
#Cache declorations
cache = Cache(aSoc,cSizeBytes,bSize,repDict[args.Replacement]) 



if __name__ == '__main__':
    cache.create_cache()
    calculate_cache_values()
    simulate()
    calculate_cpi_calues()
    
