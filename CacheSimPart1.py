import sys
import math

repDict = {'RR':"Round Robin", 'RND':"Random", 'LRU':"Least Recently Used"}
dataBus = 32

#check inputs here
#check argc
if len(sys.argv) != 11:
    print("ERROR: MISSING ARGUMENTS")
    sys.exit(1)

#check file
filetxt = open(sys.argv[2])
#check CS
#check BS
#check RP

print("Cache Simulator - CS 3853 Spring 2021 - Group XX\n")

print("Trace File: ", sys.argv[2],"\n")

print("***** Cache Input Parameters *****")
print("Cache Size:\t\t\t\t\t",sys.argv[4],"KB")
print("Block Size:\t\t\t\t\t",sys.argv[6],"bytes")
print("Associativity Size:\t\t\t",sys.argv[8])
print("Replacement Policy:\t\t\t",repDict[sys.argv[10]])

cSize = int(sys.argv[4])
cSizeBytes = pow(2, (math.log(cSize, 2)+10))
bSize = int(sys.argv[6])
aSoc = int(sys.argv[8])

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