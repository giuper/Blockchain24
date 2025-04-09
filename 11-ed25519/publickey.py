#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import decodepoint, encodepoint, edwards_double
import base64
import sys
from algosdk import mnemonic


def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK,SK[32:]

if __name__=='__main__':
    if (len(sys.argv)<2):
        print("Usage: "+sys.argv[0]+" <account name>")
        exit()

    mnemFile=sys.argv[1]+".mnem"
    SK,PK=mnemonicToPublic(mnemFile)
    print(f'{"extended SK":30s}{SK.hex()}')

    PKm=publickey(SK[0:32])
    print(f'{"The public key":30s}')
    print(f'{"from publickey method:":30s}{PKm.hex()}')
    print(f'{"from splitting extended SK:":30s}{PK.hex()}')

