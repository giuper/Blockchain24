#!/usr/bin/python3.10
##https://developer.algorand.org/docs/get-details/accounts/#transformation-private-key-to-base64-private-key

import hashlib
from ed25519new import publickey_unsafe as publickey
from ed25519new import signature_unsafe as signature
from ed25519new import checkvalid
import base64
import sys
import algosdk
from algosdk import account, mnemonic

prefix="-kdpy"

print("this script derives the public key in three different ways")
print("\tas second half of the secret key obtained from the mnemonic")
print("\tby invoking publickey method of the ED25519 library on the secret key")
print("\tby decoding the address of the account")
print("the script needs the mnemonic that is found in a file called <account name>.mnem")
print("<account name> is passed as a command line argument")

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()
accountName=sys.argv[1]
    
##files for the intermediate results 
fileSK64=accountName+prefix+".sk64"               #the base64-encoded secret key
fileSK=accountName+prefix+".sk"                   #the secret key in binary
fileAddr=accountName+prefix+".addr"               #the address
filePKSDKed25519=accountName+prefix+"-ed25519.pk" #the public key computed by the python implementation of ED25519

print("Derive secret and public key from mnem\n");
with open(accountName+".mnem",'r') as f:
    Mnem=f.read()

SK64=mnemonic.to_private_key(Mnem)                     #obtain base64-encoded secret key from mnemonic
print(f'{"SK64 from mnem:":35s}{SK64:s}')
print(f'{"written in file:":35s}{fileSK64:s}\n')
with open(fileSK64,"w") as f:
    f.write(SK64)

SK=base64.b64decode(SK64)                               #obtain the secret key by based64 decoding SK64
print(f'{"SK from decoding SK64:":35s}{SK.hex():s}')
print(f'{"written in file:":35s}{fileSK:s}\n')
with open(fileSK,"wb") as f:
    f.write(SK)
print(f'{"private key from splitting SK:":35s}{SK[0:32].hex()}')  #first half is the actual secret key
print(f'{"public key from splitting SK:":35s}{SK[32:].hex()}\n')  #second half is the public key

pk25519=publickey(SK[0:32])                                       #obtain the public key through the ED25519 python module
print(f'{"public key from SK through ed25519new:":35s}{pk25519.hex():s}')
print(f'{"written in file:":35s}{filePKSDKed25519:s}\n')
with open(filePKSDKed25519,"wb") as f:
    f.write(pk25519)

Addr=account.address_from_private_key(SK64)            #obtain address from base64-encoded secret key
print(f'{"Algorand address from SK64:":35s}{Addr:s}')
print(f'{"written in file:":35s}{fileAddr:s}')
with open(fileAddr,"w") as f:
    f.write(Addr)

AddrDec=base64.b32decode(Addr+'======')                #add padding as required by base32 encoding and then decode
print(f'{"Public key from Addr ":35s}{AddrDec[:-4].hex()}') #this will give the public key again
