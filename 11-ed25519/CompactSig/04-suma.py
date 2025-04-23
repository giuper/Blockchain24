#!/usr/bin/python3.10
from ed25519Comp import readPoint, combineHalfSig
import base64
import sys


if __name__=='__main__':

    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <source 1> <source2>")
        exit()

    R1File=sys.argv[1]+".R"
    R1=readPoint(R1File)
    R2File=sys.argv[2]+".R"
    R2=readPoint(R2File)

    S1File=sys.argv[1]+".sig"
    with open(S1File,'r') as f:
        S1=int(f.read())
    S2File=sys.argv[2]+".sig"
    with open(S2File,'r') as f:
        S2=int(f.read())

    SnonEnc=combineHalfSig(R1,S1,R2,S2,True)
    Senc=base64.b64encode(SnonEnc)
    SigFile=sys.argv[1]+sys.argv[2]+".sig"
    with open(SigFile,'w') as f:
        f.write(str(Senc,'utf-8'))
