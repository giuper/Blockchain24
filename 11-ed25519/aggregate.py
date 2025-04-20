#!/usr/bin/python3.10
from ed25519 import signature_unsafe as sign
from ed25519 import decodepoint, encodepoint, edwards_add, encodeint, decodeint, checkvalid, H, bit, Hint, scalarmult_B, l, q, isoncurve, b
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


def equalpoints(A,B):
    (x1,y1,z1,t1)=A
    (x2,y2,z2,t2)=B
    return (x1 * z2 - x2 * z1) % q == 0 and (y1 * z2 - y2 * z1) % q == 0  

if __name__=='__main__':
    if (len(sys.argv)<4):
        print("Usage: "+sys.argv[0]+" <account name> <account name> <msg file>")
        exit()

    m=b'Go SignatureSSSS'
    with open(sys.argv[3],'r') as f:
        menc=f.read()
    m=base64.b64decode(menc)
    print(f'{"message (hex):":28s}{m.hex()}')
    print(f'{"message (b64):":28s}{menc}')

    AliceSK,AlicePK=mnemonicToPublic(sys.argv[1]+".mnem")
    BobSK,BobPK=mnemonicToPublic(sys.argv[2]+".mnem")

    ha=H(AliceSK)
    sa=2 ** (b - 2) + sum(2**i * bit(ha, i) for i in range(3, b - 2))
    PA=scalarmult_B(sa)
    ra=Hint(bytes([ha[j] for j in range(b // 8, b // 4)]) + m)
    RA=scalarmult_B(ra)

    hb=H(BobSK)
    sb=2 ** (b - 2) + sum(2**i * bit(hb, i) for i in range(3, b - 2))
    PB=scalarmult_B(sb)
    rb=Hint(bytes([hb[j] for j in range(b // 8, b // 4)]) + m)
    RB=scalarmult_B(rb)


    PAgg=edwards_add(PA,PB)
    RAgg=edwards_add(RA,RB)

    HH=Hint(encodepoint(RAgg)+encodepoint(PAgg)+m)
    Sa=(ra+HH*sa)%l
    print(f'{"hint:":28s}{HH:d}')
    print(f'{"r1:":28s}{ra:d}')
    print(f'{"r2:":28s}{rb:d}')
    print(f'{"s1:":28s}{Sa:d}')
    
    Sb=(rb+HH*sb)%l
    print(f'{"s2:":28s}{Sb:d}')

    SAgg=(Sa+Sb)%l

    SigAgg=encodepoint(RAgg)+encodeint(SAgg)
    print(f'{"sig (hex):":28s}{(SigAgg[:32]).hex()}')
    print(f'{"":28s}{(SigAgg[32:]).hex()}')
    
    checkvalid(SigAgg,m,encodepoint(PAgg))
