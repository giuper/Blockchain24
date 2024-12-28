#!/usr/bin/python3.10
import base64
import sys
from Cryptodome.Hash import SHA512


def main(bytecodeFileName,ProHash=None):
    if(ProHash is not None):
        print(f'{"program hash":30s}{ProHash:s}')
        if len(ProHash)%8==0:    #padding with right number of =
            ProHashPadded=ProHash
        else:
            ProHashPadded=ProHash+"="*(8-len(ProHash)%8)
        print(f'{"program hash padded":30s}{ProHashPadded:s}')
        bProHashPadded=bytes(ProHashPadded,'utf-8')
        print(f'{"program hash padded":28s}{bProHashPadded}')
        ProHashDec=base64.b32decode(bProHashPadded)
        print(f'{"program hash decoded (hex)":30s}{ProHashDec.hex()}')
        print(f'{"re-encoded":28s}{base64.b32encode(ProHashDec)}')

    with open(bytecodeFileName,'rb') as f:   #reading the bytecodefile
        bc=f.read()
    bcPrefix=bytes("Program",'utf-8')+bc     #domain separation
    h=SHA512.new(truncate="256")
    h.update(bcPrefix)
    bcPrefixH=h.digest()
    hh=SHA512.new(truncate="256")          #computing the checksum
    hh.update(bcPrefixH)
    checksum=hh.digest()[-4:]
    final=base64.b32encode(bcPrefixH+checksum)
    print(f'{"final":28s}{final}')

if __name__ == "__main__":

    if (len(sys.argv)<2):
        print("Usage: "+sys.argv[0]+" <bytecode file> [address]")
        exit()

    bytecodeFile=sys.argv[1]+".tok"
    if (len(sys.argv)>2):
        main(bytecodeFile,sys.argv[2])
    else:
        main(bytecodeFile)

