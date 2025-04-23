#!/usr/bin/python3.10
import base64
import sys
from algosdk import encoding, constants
from algosdk.future.transaction import retrieve_from_file

if __name__=='__main__':

    if (len(sys.argv)<3):
        print("Usage: "+sys.argv[0]+" <utx file> <file for the msg>")
        exit()
    utxF=sys.argv[1]+".utx"
    msgF=sys.argv[2]

    tx=retrieve_from_file(utxF)[0]
    txn=encoding.msgpack_encode(tx)
    m=constants.txid_prefix + base64.b64decode(txn)

    print(f'{"message (hex):":28s}{m.hex()}')
    ss=str(base64.b64encode(m),'utf-8')
    print(f'{"message (b64):":28s}{ss}')
 
    with open(msgF,'w') as f:
        f.write(ss)
