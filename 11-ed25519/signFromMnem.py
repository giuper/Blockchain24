#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import signature_unsafe as signature
from ed25519 import checkvalid
import base64
import sys
from algosdk import mnemonic
from Cryptodome.Hash import SHA512


if (len(sys.argv)<4):
    print("Usage: "+sys.argv[0]+" <account name> <tok file> <data to be signed> [address of program]")
    exit()

MnemFile=sys.argv[1]+".mnem"
TokFile=sys.argv[2]+".tok"
DataToBeSigned=sys.argv[3]
if len(sys.argv)==5:
    progAddr=sys.argv[4]
else:
    progAddr=None
    

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
print(f'{"writing SK to file:":30s}{MnemFile+".sk":s}')
with open(MnemFile+".sk",'wb') as f:
    f.write(SK[0:32])

print()
print(f'{"computing hash of program:":30s}')
if progAddr is not None:
    print(f'{"starting from address:":30s}{progAddr:s}')
    if len(progAddr)%8!=0:    #padding with right number of =
        progAddr=progAddr+"="*(8-len(progAddr)%8)
    print(f'{"padded address:":30s}{progAddr:s}')
    final=base64.b32decode(progAddr)
    print(f'{"length in bytes":30s}{len(final):d}')
    print(f'{"final1":28s}{final}')
    print()

print(f'{"computing hash of program:":30s}')
print(f'{"starting from program:":30s}{TokFile:s}')
with open(TokFile,'rb') as f:
        Prog=f.read()
print(f'{"length in bytes of program":30s}{len(Prog):d}')

ProgPrefix=bytes("Program",'utf-8')+Prog     #domain separation
h=SHA512.new(truncate="256")
h.update(ProgPrefix)
ProgPrefixH=h.digest()
hh=SHA512.new(truncate="256")          #computing the checksum
hh.update(ProgPrefixH)
checksum=hh.digest()[-4:]
final2=ProgPrefixH+checksum
print(f'{"length in bytes of hash":30s}{len(final2):d}')
print(f'{"final2":28s}{final2}')
if progAddr is not None:
    if final2==final:
        print("final1==final2")
    else:
        print("final1!=final2")
        exit()

print()

unMarshaled=final2[:-4]
print(f'{"unmarshaled":28s}{unMarshaled}')  #see go-algorand/cmd/goal/tealsign.go:145
m=b'ProgData'+unMarshaled+bytes(DataToBeSigned,'utf-8') #domain separation
print(f'{"message to be signed:":28s}{m}')
s=signature(m,SK[0:32],PK)
print(f'{"signature:":28s}{s}')
checkvalid(s,m,PK)
ss64=base64.b64encode(s)
print(f'{"base64-encoded signature:":28s}{ss64}')


