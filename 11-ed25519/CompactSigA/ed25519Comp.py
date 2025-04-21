from ed25519 import *
from Cryptodome.Hash import SHA512
import base64

def mnemonicToPublic(mnemFile):
    with open(mnemFile,'r') as f:
            mnem=f.read()
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK[:32],SK[32:]

def readPoint(fileName):
    with open(fileName,'r') as f:
        x=int(f.readline())
        y=int(f.readline())
        z=int(f.readline())
        t=int(f.readline())
    return (x,y,z,t)

def writePoint(fileName,point):
    with open(fileName,'w') as f:
        f.write(str(point[0]))
        f.write('\n')
        f.write(str(point[1]))
        f.write('\n')
        f.write(str(point[2]))
        f.write('\n')
        f.write(str(point[3]))

def ks(sk):
    h=H(sk)
    k=bytes([h[j] for j in range(b // 8, b // 4)])
    s=2**254+sum(2**i * bit(h,i) for i in range(3,254))
    return s,k

def R(sk,m):
    s,k=ks(sk)
    r=Hint(k+m)
    R=scalarmult_B(r)
    return r,R

def halfSig(otherR,mysk,pk,m,verbose=False):
    s,k=ks(mysk)
    myr,myR=R(mysk,m)
    RAgg=edwards_add(otherR,myR)
    HH=Hint(encodepoint(RAgg)+encodepoint(pk)+m)
    myS=(myr+HH*s)%l
    if verbose:
        print(f'{"sk:":28s}{mysk}')
        print(f'{"hint:":28s}{HH:d}')
        print(f'{"r:":28s}{myr:d}')
        print(f'{"s:":28s}{s:d}')
        print(f'{"S:":28s}{myS:d}')
    return myS

def combineHalfSig(R1,R2,S1,S2):
    RAgg=edwards_add(R1,R2)
    R=encodepoint(RAgg)
    S=encodeint(S1+S2)
    return R+S

def combinePK(lofpk):
    sumP=(0,1,1,0)
    for pk in lofpk:
        sumP=edwards_add(sumP,pk)
    esumP=encodepoint(sumP)
    ss=SHA512.new(truncate="256")
    ss.update(esumP)
    marshall=ss.digest()
    MarshalledePS=esumP+marshall[-4:]
    Marshalled64ePS=base64.b32encode(MarshalledePS).decode('utf-8')
    return Marshalled64ePS[:-6]

def combineHalfSig(R1,S1,R2,S2,verbose=False):
    RAgg=edwards_add(R1,R2)
    R=encodepoint(RAgg)

    if verbose:
        print(f'{"s1:":28s}{S1:d}')
        print(f'{"s2:":28s}{S2:d}')

    S=encodeint(S1+S2)
    SnonEnc=R+S
    if verbose:
        print(f'{"signature (hex):":28s}{SnonEnc[:32].hex()}')
        print(f'{"":28s}{SnonEnc[32:].hex()}')
        print(f'{"":28s}{len(SnonEnc):d}')
    return SnonEnc
