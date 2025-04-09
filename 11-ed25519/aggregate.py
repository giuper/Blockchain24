#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import decodepoint, encodepoint, edwards_add
from Cryptodome.Hash import SHA512
import base64
import sys
from algosdk import mnemonic

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK,SK[32:]

def pkAlgoFormat(pk):
    ss=SHA512.new(truncate="256")
    ss.update(pk)
    marshall=ss.digest()
    marshalledPK=pk+marshall[-4:]
    return base64.b32encode(marshalledPK).decode('utf-8')

if __name__=='__main__':
    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <account name> <account name>")
        exit()

    AliceSK,AlicePK=mnemonicToPublic(sys.argv[1]+".mnem")
    BobSK,BobPK=mnemonicToPublic(sys.argv[2]+".mnem")

    PA=decodepoint(AlicePK)
    PB=decodepoint(BobPK)

    PS=encodepoint(edwards_add(PA,PB))
    print(f'{"Alice public key:":30s}{AlicePK.hex()}')
    print(f'{"":30s}{pkAlgoFormat(AlicePK)}')
    
    print(f'{"Bob public key:":30s}{BobPK.hex()}')
    print(f'{"":30s}{pkAlgoFormat(BobPK)}')

    print(f'{"Aggregate public key:":30s}{PS.hex()}')
    print(f'{"":30s}{pkAlgoFormat(PS)}')
    
