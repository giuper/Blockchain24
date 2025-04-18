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

    return (x1*z2-x2*z1)%q==0 and (y1*z2-y2*z1)%q==0


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

    print("Step 1: public and secret key from mnem")
    mnemFile=sys.argv[1]+".mnem"
    SK,PK=mnemonicToPublic(mnemFile)
    print(f'{"The secret key in hex":30s}{SK.hex()}')

    sek=hashlib.sha512(SK).digest()
    #using a different library to compute the hash
    #s512=SHA512.new() 
    #s512.update(SK)
    #seka=s512.digest()

    #checking that the two libraries give the same value
    #print(sek.hex())
    #print(seka.hex())

    print(f'{"The base point B"}')
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


    print("\nStep 2: public from addr")

    addrFile=sys.argv[1]+".addr"
    with open(addrFile,'r') as f:
        addr=f.read()
    PKaddr=(base64.b32decode(addr+'======'))[:-4]
    print(f'{"The public key in hex":30s}')
    print(f'{"from addr file:":30s}{PKaddr.hex()}')
    addrDecP=decodepoint(PKaddr)
    if not checkEqualityPoints(PS,addrDecP):
        print("Errore!")
        exit()
    print(f'{"The point from the addr"}')
    print(f'{"":20s}{"X":10s}{addrDecP[0]}')
    print(f'{"":20s}{"Y":10s}{addrDecP[1]}')
    print(f'{"":20s}{"Z":10s}{addrDecP[2]}')
    print(f'{"":20s}{"T":10s}{addrDecP[3]}')
    print(f'{"The point encoded":30s}{PKaddr.hex()}')

    print("\nStep 3: public from SK thorugh the package")
    PKm=publickey(SK)
    addrDecP=decodepoint(PKm)
    if not checkEqualityPoints(PS,addrDecP):
        print("Errore!")
        exit()
    print(f'{"The point from the addr"}')
    print(f'{"":20s}{"X":10s}{addrDecP[0]}')
    print(f'{"":20s}{"Y":10s}{addrDecP[1]}')
    print(f'{"":20s}{"Z":10s}{addrDecP[2]}')
    print(f'{"":20s}{"T":10s}{addrDecP[3]}')
    print(f'{"The point encoded":30s}{PKm.hex()}')

    print("\nStep 4: public from second half of SK")
    addrDecP=decodepoint(PK)
    if not checkEqualityPoints(PS,addrDecP):
        print("Errore!")
        exit()
    print(f'{"The point from the addr"}')
    print(f'{"":20s}{"X":10s}{addrDecP[0]}')
    print(f'{"":20s}{"Y":10s}{addrDecP[1]}')
    print(f'{"":20s}{"Z":10s}{addrDecP[2]}')
    print(f'{"":20s}{"T":10s}{addrDecP[3]}')
    print(f'{"The point encoded":30s}{PK.hex()}')


    print("\nStep 5: address from point computed at Step 1")
    ePS=encodepoint(PS)
    ss=SHA512.new(truncate="256")
    ss.update(ePS)
    marshall=ss.digest()
    MarshalledePS=ePS+marshall[-4:]
    print(f'{"from addr file:":30s}{addr}')
    Marshalled64ePS=base64.b32encode(MarshalledePS).decode('utf-8')
    print(f'{"from point":30s}{Marshalled64ePS[:-6]}')
