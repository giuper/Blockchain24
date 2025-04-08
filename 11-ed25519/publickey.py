#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import decodepoint, encodepoint
import base64
import sys
from algosdk import mnemonic


if (len(sys.argv)<2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()

MnemFile=sys.argv[1]+".mnem"
with open(MnemFile,'r') as f:
        Mnem=f.read()
SK64=mnemonic.to_private_key(Mnem)
print(f'{"b64 secret key from mnem":30s}{SK64}')
SK=base64.b64decode(SK64) #see https://developer.algorand.org/docs/get-details/accounts/
print(f'{"extended SK":30s}{SK.hex()}')

PK=publickey(SK[0:32])
print(f'{"The public key":30s}')
print(f'{"from publickey method:":30s}{PK.hex()}')
print(f'{"from splitting extended SK:":30s}{SK[32:].hex()}')

