#!/usr/bin/python3.10
from ed25519 import decodepoint
from ed25519Comp import combinePK
from conversions import algoaddtopoint
import base64
import sys

if __name__=='__main__':
    if (len(sys.argv)<4):
        print("Usage: "+sys.argv[0]+" <source1> <source2> <dest>")
        exit()

    lofpk=[]
    for i in [1,2]: 
        with open(sys.argv[i]+".addr",'r') as f:
                addr=f.read()
        print(f'{"source pk":25s}{addr}')
        point=algoaddtopoint(addr)
        lofpk.append(point)
    pk=combinePK(lofpk)
    with open(sys.argv[3]+".addr",'w') as f:
        f.write(pk)
    print(f'{"dest pk":25s}{pk}')
