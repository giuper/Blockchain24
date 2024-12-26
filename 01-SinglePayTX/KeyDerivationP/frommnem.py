#!/usr/bin/python3.10

import hashlib
from ed25519new import publickey_unsafe as publickey
from ed25519new import signature_unsafe as signature
from ed25519new import checkvalid
import base64
import sys
import algosdk
from algosdk import account, mnemonic

folder="../Accounts/"
prefix="-kdpy"
if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    print("keys are written in folder",folder)
    exit()
accountName=sys.argv[1]
fileSK64=folder+accountName+prefix+".sk64"
fileSK=folder+accountName+prefix+".sk"
fileAddr=folder+accountName+prefix+".addr"
filePKHex=folder+accountName+prefix+".pkhex"
filePK=folder+accountName+prefix+".pk"
filePKSDKed25519=folder+accountName+prefix+"-ed25519.pk"

print("Derive secret and public key from mnem\n");
with open(accountName+".mnem",'r') as f:
    Mnem=f.read()

SK64=mnemonic.to_private_key(Mnem)
Addr=account.address_from_private_key(SK64)
print(f'{"SK64 from mnem:":35s}{SK64:s}')
print(f'{"written in file:":35s}{fileSK64:s}\n')
with open(fileSK64,"w") as f:
    f.write(SK64)

SK=base64.b64decode(SK64)
print(f'{"SK from decoding SK64:":35s}{SK.hex():s}')
print(f'{"written in file:":35s}{fileSK:s}\n')
with open(fileSK,"wb") as f:
    f.write(SK)
print(f'{"private key from splitting SK:":35s}{SK[0:32].hex()}')
print(f'{"public key from splitting SK:":35s}{SK[32:].hex()}\n')

pk25519=publickey(SK[0:32])
print(f'{"PK from SK through ed25519new:":35s}{pk25519.hex():s}')
print(f'{"written in file:":35s}{filePKSDKed25519:s}\n')
with open(filePKSDKed25519,"wb") as f:
    f.write(pk25519)

Addr=account.address_from_private_key(SK64)
print(f'{"Algorand address from SK64:":35s}{Addr:s}')
print(f'{"written in file:":35s}{fileAddr:s}')
with open(fileAddr,"w") as f:
    f.write(Addr)

AddrDec=base64.b32decode(Addr+'======')
print(f'{"Public key from Addr ":35s}{AddrDec[:-4].hex()}')
