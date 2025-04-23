#!/usr/bin/python3.10

import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn, write_to_file
from utilities import algodAddress, algodToken


def payTX(sAddr,rAddr,amount,algodClient):

    params = algodClient.suggested_params()

    unsignedTx=PaymentTxn(
        sender=sAddr,
        sp=params,
        receiver=rAddr,
        amt=amount,
        note=b"Ciao Pino",
    )
    return unsignedTx

def main():
    if len(sys.argv)!=4:
        print("usage: "+sys.argv[0]+" <file with sender addr> <file with receiver addr> <output tx file>")
        exit()

    amount=1_000_000

    algodClient = algod.AlgodClient(algodToken,algodAddress)

    senderAddrF=sys.argv[1]+".addr"
    with open(senderAddrF,'r') as f:
        sAddr=f.read()
    print(f'{"Sender address:":32s}{sAddr:s}')

    receiverAddrF=sys.argv[2]+".addr"
    with open(receiverAddrF,'r') as f:
        rAddr=f.read()
    print(f'{"Receiver address:":32s}{rAddr:s}')

    utx=payTX(sAddr,rAddr,amount,algodClient)
    write_to_file([utx],sys.argv[3])

if __name__=='__main__':
    main()
