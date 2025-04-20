#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import signature_unsafe as signature
from ed25519 import edwards_add, bit, encodepoint, encodeint
from ed25519 import b, l, q
import base64
import sys
from algosdk import mnemonic

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK[:32],SK[32:]

def readPoint(fileName):
    with open(fileName,'r') as f:
        x=int(f.readline())
        y=int(f.readline())
        z=int(f.readline())
        t=int(f.readline())
    return (x,y,z,t)


if __name__=='__main__':

    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <source 1> <source2>")
        exit()

    R1File=sys.argv[1]+".R"
    R1=readPoint(R1File)
    R2File=sys.argv[2]+".R"
    R2=readPoint(R2File)

    RAgg=edwards_add(R1,R2)
    R=encodepoint(RAgg)

    S1File=sys.argv[1]+".sig"
    with open(S1File,'r') as f:
        S1=int(f.read())
    print(f'{"s1:":28s}{S1:d}')

    S2File=sys.argv[2]+".sig"
    with open(S2File,'r') as f:
        S2=int(f.read())
    print(f'{"s2:":28s}{S2:d}')

    S=encodeint(S1+S2)
    SnonEnc=R+S
    print(f'{"signature (hex):":28s}{SnonEnc[:32].hex()}')
    print(f'{"":28s}{SnonEnc[32:].hex()}')
    print(f'{"":28s}{len(SnonEnc):d}')
    Senc=base64.b64encode(SnonEnc)
    SigFile=sys.argv[1]+sys.argv[2]+".sig"
    with open(SigFile,'w') as f:
        f.write(str(Senc,'utf-8'))
