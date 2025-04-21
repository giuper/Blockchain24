#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import signature_unsafe as signature
from ed25519 import edwards_add, H, bit, Hint, encodepoint, decodepoint
from ed25519 import b, l, q
import base64
import sys
from algosdk import mnemonic
from Cryptodome.Hash import SHA512

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

    if (len(sys.argv)<5):
        print("Usage: "+sys.argv[0]+" <source 1> <source2> <pAgg file> <message file> ")
        exit()

    MnemFile=sys.argv[1]+".mnem"
    SK,PK=mnemonicToPublic(MnemFile)

    r1File=sys.argv[1]+".r"
    with open(r1File,'r') as f:
        r1=int(f.read())
    R1File=sys.argv[1]+".R"
    R1=readPoint(R1File)

    R2File=sys.argv[2]+".R"
    R2=readPoint(R2File)

    with open(sys.argv[3]+".addr",'r') as f:
        PAggAddr=f.read()
    PAggEnc=(base64.b32decode(PAggAddr+'======'))[:-4]
    print(f'{"public (hex)":28s}{PAggEnc.hex()}')
    PAgg=decodepoint(PAggEnc)

    with open(sys.argv[4],'r') as f:
        ss=f.read()
    m=base64.b64decode(ss)
    print(f'{"message (hex)":28s}{m.hex()}')
    print(f'{"message (b64)":28s}{ss}')

    RAgg=edwards_add(R1,R2)
    
    h=H(SK)
    HH=Hint(encodepoint(RAgg)+encodepoint(PAgg)+m)
    s=2 ** (b - 2) + sum(2**i * bit(h, i) for i in range(3, b - 2))
    S=(r1+HH*s)%l
    print(f'{"sk:":28s}{SK}')
    print(f'{"hint:":28s}{HH:d}')
    print(f'{"r:":28s}{r1:d}')
    print(f'{"s:":28s}{s:d}')
    print(f'{"S:":28s}{S:d}')
    
    SigFile=sys.argv[1]+".sig"
    with open(SigFile,'w') as f:
        f.write(str(S))

