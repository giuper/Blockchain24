#!/usr/bin/python3.10
from ed25519 import decodepoint, encodepoint
from ed25519 import edwards_add, H, bit, scalarmult_B
from Cryptodome.Hash import SHA512
import base64
import sys
from algosdk import mnemonic

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK[:32],SK[32:]

def extractSK(sk):
    h=H(sk)
    s=2**(254) + sum(2**i*bit(h,i) for i in range(3,254))
    k=bytes([h[j] for j in range(32,64)])
    return (s,k)


if __name__=='__main__':
    if (len(sys.argv)<4):
        print("Usage: "+sys.argv[0]+" <source1> <source2> <dest>")
        exit()

    sumP=(0,1,1,0)
    for i in [1,2]: 
        with open(sys.argv[i]+".addr",'r') as f:
                addr=f.read()
                print(f'{"source pk":25s}{addr}')
                addrHex=(base64.b32decode(addr+'======'))[:-4]
                addrP=decodepoint(addrHex)
                sumP=edwards_add(sumP,addrP)
    esumP=encodepoint(sumP)
    ss=SHA512.new(truncate="256")
    ss.update(esumP)
    marshall=ss.digest()
    MarshalledePS=esumP+marshall[-4:]
    Marshalled64ePS=base64.b32encode(MarshalledePS).decode('utf-8')
    with open(sys.argv[3]+".addr",'w') as f:
        f.write(Marshalled64ePS[:-6])
    print(f'{"dest pk":25s}{Marshalled64ePS[:-6]}')
