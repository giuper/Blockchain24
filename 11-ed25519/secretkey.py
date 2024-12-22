#!/usr/bin/python3.10

import sys
import base64
from algosdk import account, mnemonic

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()

account=sys.argv[1]

mnemF=account+".mnem"
with open(mnemF,'r') as f:
    Mnem=f.read()

SK64=mnemonic.to_private_key(Mnem)
print(creatorSK64)
with open(account+".sk64","w") as f:
    f.write(SK64)

SK=base64.b64decode(creatorSK64)
##print(creatorSK)  
with open(account+".skk","wb") as f:
    f.write(SK)

Addr=account.address_from_private_key(SK64)
print(Addr)
with open(account+".addr","w") as f:
    f.write(Addr)

##same effect can be obtained with algokey import
