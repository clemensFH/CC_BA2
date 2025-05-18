from cbor2 import dump, dumps
import json

def readFromFile(filename: str, outputfile = ""):
    with open(f'./data/{filename}', 'r') as fobj:
        content = json.load(fobj)

    print(type(content[0]))
    output = dumps(content)
    if not outputfile:
        return output
    else:
        with open(f'./data/{outputfile}', "wb") as fobj:
            fobj.write(output)
        return True

    

class CBORIterator():

    def __init__(self, content: bytes):
        self.content = content
        self.idx = -1
        self.length = len(content)
    
    def getNextByte(self):
        if self.idx + 1 > self.length - 1:
            raise ValueError("End of content reached!")

        c = self.content[self.idx + 1]
        self.idx+=1
        return c
    
    def getNextBytes(self, n: int):
        if self.idx + n > self.length - 1:
            raise ValueError("To much steps - End of content reached!")

        ns = self.content[self.idx + 1: self.idx + n+1] # +1 weil Ende exklusiv
        self.idx+=n
        return ns
    
    def ReachedEnd(self):
        return self.idx == self.length - 1
    
    def getRemainingBytes(self):
        return self.length - 1 - self.idx