
HASHES = {}

lines = []
with open('./data/hashes.txt', 'r') as fobj:
    lines = fobj.readlines()

for line in lines:
    params = line.split(":")
    mb = int(params[0].replace("MB", "").strip())
    hsh = params[1].strip()
    HASHES[mb] = hsh

#print(HASHES)
