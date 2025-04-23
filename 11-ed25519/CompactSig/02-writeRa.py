#!/usr/bin/python3.10
from ed25519Comp import R, writePoint
from conversions import mnemonictokeys
import base64
import sys
from algosdk import mnemonic

if __name__=='__main__':
    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <account name> <message>")
        exit()

    with open(sys.argv[2],'r') as f:
        ss=f.read()
    m=base64.b64decode(ss)
    print(f'{"message (hex)":28s}{m.hex()}')
    print(f'{"message (b64)":28s}{ss}')

    mnemFile=sys.argv[1]+".mnem"
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK,PK=mnemonictokeys(mnem)

    r,RA=R(SK,m)
    writePoint(sys.argv[1]+".R",RA)
