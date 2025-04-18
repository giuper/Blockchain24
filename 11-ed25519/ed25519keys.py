#!/usr/bin/python3.10
from ed25519 import publickey_unsafe as publickey
from ed25519 import decodepoint, encodepoint, edwards_double, H, B, bit, scalarmult_B, q
import base64
import sys
from algosdk import mnemonic
from Cryptodome.Hash import SHA512
import hashlib

def checkEqualityPoints(P,Q):
    (x1,y1,z1,t1)=P
    (x2,y2,z2,t2)=Q

    if (x1*z2-x2*z1)%q!=0:
        return "F"
    if (y1*z2-y2*z1)%q!=0:
        return "F"
    return "T"

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64enc=mnemonic.to_private_key(mnem)
    SK64=base64.b64decode(SK64enc) 
    return SK64[:32],SK64[32:]

if __name__=='__main__':
    if (len(sys.argv)<2):
        print("Usage: "+sys.argv[0]+" <account name>")
        exit()

    mnemFile=sys.argv[1]+".mnem"
    SK,PK=mnemonicToPublic(mnemFile)
    print(f'{"The secret key in hex":30s}{SK.hex()}')

    sek=hashlib.sha512(SK).digest()
    #using a different library to compute the has
    #s512=SHA512.new() 
    #s512.update(SK)
    #seka=s512.digest()

    #checking that the two libraries give the same value
    #print(sek.hex())
    #print(seka.hex())

    print(f'{"The point B from the definition"}')
    print(f'{"":20s}{"X":10s}{B[0]}')
    print(f'{"":20s}{"Y":10s}{B[1]}')
    print(f'{"":20s}{"Z":10s}{B[2]}')
    print(f'{"":20s}{"T":10s}{B[3]}')

    #the first 256 bits of sek give an integer s
    s=2**(254) + sum(2**i*bit(sek,i) for i in range(3,254))
    print(f'{"The 256-bit multiplier s":30s}{s:d}')

    #the point that constitute the public key is s*B
    #B is a public point from Ed25519 definition
    PS=scalarmult_B(s)
    print(f'{"The point s*B in the public key"}')
    print(f'{"":20s}{"X":10s}{PS[0]}')
    print(f'{"":20s}{"Y":10s}{PS[1]}')
    print(f'{"":20s}{"Z":10s}{PS[2]}')
    print(f'{"":20s}{"T":10s}{PS[3]}')
    print(f'{"The point s*B encoded":35s}{encodepoint(PS).hex()}')


    print()


    addrFile=sys.argv[1]+".addr"
    with open(addrFile,'r') as f:
        addr=f.read()
    PKaddr=(base64.b32decode(addr+'======'))[:-4]

    PKm=publickey(SK)
    print(f'{"The public key in hex":30s}')
    print(f'{"":5s}{"from addr file:":30s}{PKaddr.hex()}')
    print(f'{"":5s}{"from publickey method:":30s}{PKm.hex()}')
    print(f'{"":5s}{"from splitting extended SK:":30s}{PK.hex()}')

    print(f'{"The public key as a point":30s}')
    
    toPrint=[["from addr file",PKaddr],["from public method",PKm],["from splitting extended SK",PK]]
    for (msg,binP) in toPrint:
        addrDecP=decodepoint(binP)
        ff=checkEqualityPoints(PS,addrDecP)
        print(f'{ff:5s}{msg:30s}')

        for i in range(4):
            print(f'{"":10}{addrDecP[i]}')
    

    print(f'{"The public key in Algorand format":30s}')
    ss=SHA512.new(truncate="256")
    ss.update(PKm)
    marshall=ss.digest()
    MarshalledPKm=PKm+marshall[-4:]
    #print(f'{"computed:":30s}{MarshalledPKm}')
    print(f'{"from addr file:":30s}{addr}')
    Marshalled64PKm=base64.b32encode(MarshalledPKm).decode('utf-8')
    print(f'{"in Algorand format:":30s}{Marshalled64PKm}')
