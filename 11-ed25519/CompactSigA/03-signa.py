#!/usr/bin/python3.10
from ed25519Comp import halfSig, readPoint
import sys
import base64
from conversions import algoaddtopoint, mnemonictokeys

    

if __name__=='__main__':

    if (len(sys.argv)<5):
        print("Usage: "+sys.argv[0]+" <source 1> <source2> <pAgg file> <message file> ")
        exit()

    mnemFile=sys.argv[1]+".mnem"
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK,PK=mnemonictokeys(mnem)

    R2File=sys.argv[2]+".R"
    R2=readPoint(R2File)

    
    addrFile=sys.argv[3]+".addr"
    with open(addrFile,'r') as f:
        addr=f.read()
    PAgg=algoaddtopoint(addr)

    with open(sys.argv[4],'r') as f:
        ss=f.read()
    m=base64.b64decode(ss)
    print(f'{"message (hex)":28s}{m.hex()}')
    print(f'{"message (b64)":28s}{ss}')

    S=halfSig(R2,SK,PAgg,m,True)
    SigFile=sys.argv[1]+".sig"
    with open(SigFile,'w') as f:
        f.write(str(S))
