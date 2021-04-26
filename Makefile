
INTERP=python3

SIM=CacheSimPart1.py

# python3 CacheSimPart1.py -f TinyTrace.trc -s 512 -b 16 -a 2 -r RR
test:
	$(INTERP) $(SIM) -f Trace1.trc -s 512 -b 16 -a 2 -r LRU