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
filetxt = open(args.FileTrace)
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