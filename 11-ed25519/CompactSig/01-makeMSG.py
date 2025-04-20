#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import signature_unsafe as signature
from ed25519 import checkvalid
import base64
import sys
from algosdk import mnemonic
from Cryptodome.Hash import SHA512

if __name__=='__main__':

    if (len(sys.argv)<4):
        print("Usage: "+sys.argv[0]+" <tok file> <data to be signed> <msg file>")
        exit()

    TokFile=sys.argv[1]+".tok"
    DataToBeSigned=sys.argv[2]
    MsgFile=sys.argv[3]
    
    print(f'{"computing hash of program:":28s}')
    print(f'{"starting from program:":28s}{TokFile:s}')
    with open(TokFile,'rb') as f:
            Prog=f.read()
    print(f'{"length in bytes of program":28s}{len(Prog):d}')
    
    ProgPrefix=bytes("Program",'utf-8')+Prog     #domain separation
    h=SHA512.new(truncate="256")
    h.update(ProgPrefix)
    ProgPrefixH=h.digest()
    hh=SHA512.new(truncate="256")          #computing the checksum
    hh.update(ProgPrefixH)
    checksum=hh.digest()[-4:]
    final2=ProgPrefixH+checksum
    print(f'{"length in bytes of hash":28s}{len(final2):d}')
    print(f'{"final2":28s}{final2}')
    
    unMarshaled=final2[:-4]
    print(f'{"unmarshaled":28s}{unMarshaled}')  #see go-algorand/cmd/goal/tealsign.go:145
    m=b'ProgData'+unMarshaled+bytes(DataToBeSigned,'utf-8') #domain separation
    print(f'{"message (hex):":28s}{m.hex()}')
    ss=str(base64.b64encode(m),'utf-8')
    print(f'{"message (b64):":28s}{ss}')
    
    with open(MsgFile,'w') as f:
        f.write(ss)
