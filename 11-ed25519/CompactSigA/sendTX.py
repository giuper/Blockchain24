#!/usr/bin/python3.10

import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, retrieve_from_file, SignedTransaction
from utilities import algodAddress, algodToken, wait_for_confirmation




def main():
    if len(sys.argv)!=3:
        print("usage: "+sys.argv[0]+" <file with TX> <file with signature>")
        exit()

    algodClient = algod.AlgodClient(algodToken,algodAddress)

    txF=sys.argv[1]
    sigF=sys.argv[2]+".sig"

    tx=retrieve_from_file(txF+".utx")[0]
    with open(sigF,'r') as f:
        encSig=f.read()
    print(f'{"signature (b64):":28s}{encSig}')
    sig=base64.b64decode(encSig)
    print(f'{"signature (hex):":28s}{(sig[:32]).hex()}')
    print(f'{"":28s}{(sig[32:]).hex()}')
    stx=SignedTransaction(tx,encSig,None)
    write_to_file([stx],txF+".stx")

    txid=algodClient.send_transaction(stx)
    print(f'{"Signed transaction with txID:":32s}{txid:s}')
    print()

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

if __name__=='__main__':
    main()
