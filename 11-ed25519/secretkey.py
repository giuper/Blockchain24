#!/usr/bin/python3.10

import sys
import base64
from algosdk import account, mnemonic

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()

acct=sys.argv[1]

mnemF=acct+".mnem"
with open(mnemF,'r') as f:
    Mnem=f.read()

SK64=mnemonic.to_private_key(Mnem)
print(f'{"The secret key from mnem":28s}{SK64}')
print(f'{"Found in file":28s}{acct+".sk64"}')
with open(acct+".sk64","w") as f:
    f.write(SK64)

SK=base64.b64decode(SK64)
with open(acct+".skk","wb") as f:
    f.write(SK)
print(f'{"Binary key found in file":28s}{acct+".skk"}')

Addr=account.address_from_private_key(SK64)
print(f'{"The address from the secret key":28s}{Addr}')
print(f'{"Found in file":28s}{acct+".addr"}')
with open(acct+".addr","w") as f:
    f.write(Addr)

##same effect can be obtained with algokey import
##but without having to install a node
