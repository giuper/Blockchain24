#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import signature_unsafe as signature
from ed25519 import edwards_add, H, bit, Hint, encodepoint, decodepoint, encodeint, checkvalid
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

    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <Addr file> <Msg file> <Sig file>")
        exit()

    print("Verifiying")
    print(f'{"signature file":28s}{sys.argv[3]+".sig"}')
    print("against")
    print(f'{"message file":28s}{sys.argv[2]}')
    print(f'{"public key file":28s}{sys.argv[1]+".addr"}')

    with open(sys.argv[1]+".addr",'r') as f:
        PAggAddr=f.read()
    PAggEnc=(base64.b32decode(PAggAddr+'======'))[:-4]
    print(f'{"public (hex)":28s}{PAggEnc.hex()}')
    pk=decodepoint(PAggEnc)
    pk=PAggEnc

    with open(sys.argv[2],'r') as f:
        encM=f.read()
    m=base64.b64decode(encM)
    print(f'{"message (hex):":28s}{m.hex()}')

    with open(sys.argv[3]+".sig",'r') as f:
        encSig=f.read()
    sig=base64.b64decode(encSig)
    print(f'{"signature (hex):":28s}{(sig[:32]).hex()}')
    print(f'{"":28s}{(sig[32:]).hex()}')
    checkvalid(sig,m,pk)
