from cbor2 import dump, dumps

def readFromFile(filename: str, outputfile = ""):
    with open(f'./data/{filename}') as fobj:
        content = fobj.read()
    
    output = dumps(content).hex()
    if not outputfile:
        return output
    else:
        with open(f'./data/{outputfile}', "w") as fobj:
            fobj.write(output)
        return True
    

class cborIterator():

    def __init__(self, content: str):
        self.content = content
        self.idx = -1
        self.length = len(content)
    
    def getNextSign(self):
        if self.idx + 1 > self.length - 1:
            raise ValueError("End of content reached!")

        c = self.content[self.idx + 1]
        self.idx+=1
        return c
    
    def getNextSigns(self, n: int):
        if self.idx + n > self.length - 1:
            raise ValueError("To much steps - End of content reached!")

        ns = self.content[self.idx + 1: self.idx + n+1]
        self.idx+=n
        return ns
    
    def ReachedEnd(self):
        return self.idx == self.length - 1
    
    def getRemainingSigns(self):
        return self.length - 1 - self.idx