from algosdk import mnemonic
import base64
from ed25519 import decodepoint
from Cryptodome.Hash import SHA512

def hashfromencodedh(eHash,verbose=False):
        if verbose:
            print(f'{"computing hash of program:":28s}')
            print(f'{"starting from encoded hash:":28s}{progAddr:s}')
        if len(eHash)%8!=0:
            eHash=eHash+"="*(8-len(eHash)%8)
        if verbose:
            print(f'{"padded address:":28s}{eHash:s}')
        hashV=base64.b32decode(eHash)
        if verbose:
            print(f'{"length in bytes":28s}{len(hashV):d}')
            print(f'{"hashV":28s}{hashV}')
        return hashV

def hashfrombytecode(Prog,verbose=False):
    ProgPrefix=bytes("Program",'utf-8')+Prog     #domain separation
    h=SHA512.new(truncate="256")
    h.update(ProgPrefix)
    ProgPrefixH=h.digest()
    hh=SHA512.new(truncate="256")          #computing the checksum
    hh.update(ProgPrefixH)
    checksum=hh.digest()[-4:]
    final2=ProgPrefixH+checksum
    if verbose:
        print(f'{"length in bytes of hash":28s}{len(final2):d}')
        print(f'{"final2":28s}{final2}')
    return final2
    

def algoaddtopoint(addr):
    addrHex=(base64.b32decode(addr+'======'))[:-4]
    addrP=decodepoint(addrHex)
    return addrP

def mnemonictokeys(mnem):
    SK64=mnemonic.to_private_key(mnem)
    SK=base64.b64decode(SK64) 
    return SK[:32],SK[32:]
