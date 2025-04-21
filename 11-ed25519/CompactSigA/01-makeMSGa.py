#!/usr/bin/python3.10
import base64
import sys
from conversions import hashfrombytecode, hashfromencodedh

if __name__=='__main__':

    if (len(sys.argv)<4):
        print("Usage: "+sys.argv[0]+" <tok file> <data to be signed> <msg file> [encodedHash]")
        exit()

    TokFile=sys.argv[1]+".tok"
    DataToBeSigned=sys.argv[2]
    MsgFile=sys.argv[3]
    if len(sys.argv)==5:
        progAddr=sys.argv[4]
        hashV=hashfromencodedh(progAddr)

    
    print(f'{"computing hash of program:":28s}')
    print(f'{"starting from program:":28s}{TokFile:s}')
    with open(TokFile,'rb') as f:
            Prog=f.read()
    print(f'{"length in bytes of program":28s}{len(Prog):d}')
    
    final2=hashfrombytecode(Prog)
    unMarshaled=final2[:-4]
    print(f'{"unmarshaled":28s}{unMarshaled}')  #see go-algorand/cmd/goal/tealsign.go:145
    m=b'ProgData'+unMarshaled+bytes(DataToBeSigned,'utf-8') #domain separation
    print(f'{"message (hex):":28s}{m.hex()}')
    ss=str(base64.b64encode(m),'utf-8')
    print(f'{"message (b64):":28s}{ss}')
    
    with open(MsgFile,'w') as f:
        f.write(ss)
