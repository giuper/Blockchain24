#!/usr/bin/python3.10
from ed25519 import signature_unsafe as sign
from ed25519 import H, bit, Hint, scalarmult_B, b
import base64
import sys
from algosdk import mnemonic

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK[:32],SK[32:]

if __name__=='__main__':
    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <account name> <message>")
        exit()


    with open(sys.argv[2],'r') as f:
        ss=f.read()
    m=base64.b64decode(ss)
    print(f'{"message (hex)":28s}{m.hex()}')
    print(f'{"message (b64)":28s}{ss}')

    SK,PK=mnemonicToPublic(sys.argv[1]+".mnem")
    ha=H(SK)
    ra=Hint(bytes([ha[j] for j in range(b // 8, b // 4)]) + m)
    RA=scalarmult_B(ra)
    with open(sys.argv[1]+".r",'w') as f:
        f.write(str(ra)+"\n")
    with open(sys.argv[1]+".R",'w') as f:
        f.write(str(RA[0]))
        f.write('\n')
        f.write(str(RA[1]))
        f.write('\n')
        f.write(str(RA[2]))
        f.write('\n')
        f.write(str(RA[3]))
