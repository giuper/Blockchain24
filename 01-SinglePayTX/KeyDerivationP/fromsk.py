#!/usr/bin/python3.10

import hashlib
from ed25519new import publickey_unsafe as publickey
from ed25519new import signature_unsafe as signature
from ed25519new import checkvalid
import base64
import sys
import algosdk
from algosdk import account, mnemonic

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()
folder="../KEYS/"
prefix="-kdpy"
cprefix="-kdcc"
accountName=sys.argv[1]
fileSK=folder+accountName+cprefix+".sk"
filePKSDKed25519=folder+accountName+prefix+"-ed25519.pk"
#fileSK64=folder+accountName+prefix+".sk64"
#fileAddr=folder+accountName+prefix+".addr"
#filePKHex=folder+accountName+prefix+".pkhex"
#filePK=folder+accountName+prefix+".pk"

with open(fileSK,'rb') as f:
    SK=f.read()

print(f'{"SK:":35s}{SK.hex():s}')
print(f'{"read from file:":35s}{fileSK:s}\n')
print(f'{"private key from splitting SK:":35s}{SK[0:32].hex()}')
print(f'{"public key from splitting SK:":35s}{SK[32:].hex()}\n')

pk25519=publickey(SK[0:32])
print(f'{"PK from SK through ed25519new:":35s}{pk25519.hex():s}')
print(f'{"written in file:":35s}{filePKSDKed25519:s}\n')
with open(filePKSDKed25519,"wb") as f:
    f.write(pk25519)
