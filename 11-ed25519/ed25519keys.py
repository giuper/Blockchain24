#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import decodepoint, encodepoint, edwards_double, H
import base64
import sys
from algosdk import mnemonic
from Cryptodome.Hash import SHA512



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
    print(f'{"extended SK":30s}{SK[:32].hex()}')
    print(f'{"":30s}{SK[32:].hex()}')

    addrFile=sys.argv[1]+".addr"
    with open(addrFile,'r') as f:
        addr=f.read()
    addrDec=(base64.b32decode(addr+'======'))[:-4]

    PKm=publickey(SK[0:32])
    print(f'{"The public key in hex":30s}')
    print(f'{"from addr file:":30s}{addrDec.hex()}')
    print(f'{"from publickey method:":30s}{PKm.hex()}')
    print(f'{"from splitting extended SK:":30s}{PK.hex()}')

    print(f'{"The public key in Algorand format":30s}')
    ss=SHA512.new(truncate="256")
    ss.update(PKm)
    marshall=ss.digest()
    MarshalledPKm=PKm+marshall[-4:]
    #print(f'{"computed:":30s}{MarshalledPKm}')
    print(f'{"from addr file:":30s}{addr}')
    Marshalled64PKm=base64.b32encode(MarshalledPKm).decode('utf-8')
    print(f'{"in Algorand format:":30s}{Marshalled64PKm}')
    

    
    
