#!/usr/bin/python3.10

import sys
import base64
#from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import write_to_file, ApplicationNoOpTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):


    params=algodClient.suggested_params()
    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address:":20s}{Addr:s}')
    print(f'{"Calling app:":20s}{index:d}')

    signature64='MkiiTrSOF15IlUIWt/REzDOboC1Us064NHpzW5iYU5t9vGcgAGKICT0qtn8Sr7SmBdU9+f1eLlWjVVYQGmlIAA=='
    signature=base64.b64decode(signature64)
    print(f'{"sig64":20s}{signature64}')
    print(f'{"sig":20s}{signature}')


    Arg11=1
    appArgs1=[signature,Arg11.to_bytes(8,'big')]
    utx1=ApplicationNoOpTxn(Addr,params,index,appArgs1)

    Arg20=44
    Arg21=0
    appArgs2=[Arg20.to_bytes(8,'big'),Arg21.to_bytes(8,'big')]
    utx2=ApplicationNoOpTxn(Addr,params,index,appArgs2)

    Arg30=33
    Arg31=0
    appArgs3=[Arg30.to_bytes(8,'big'),Arg31.to_bytes(8,'big')]
    utx3=ApplicationNoOpTxn(Addr,params,index,appArgs3)

    group=[utx2,utx3,utx1]
    gid=transaction.calculate_group_id(group)
    utx1.group=gid
    utx2.group=gid
    utx3.group=gid
    write_to_file(group,"TX/group.utx")
    print("writing unsigned transactions in TX/group.utx")

    sutx1=utx1.sign(SK)
    print(f'{"sutx1":20s}{sutx1.get_txid():s}')
    #print(f'{" ":20s}{signature:s}')
    print(f'{" ":20s}{Arg11:d}')

    sutx2=utx2.sign(SK)
    print(f'{"sutx2":20s}{sutx2.get_txid():s}')
    print(f'{" ":20s}{Arg20:d}')
    print(f'{" ":20s}{Arg21:d}')

    sutx3=utx3.sign(SK)
    print(f'{"sutx3":20s}{sutx3.get_txid():s}')
    print(f'{" ":20s}{Arg30:d}')
    print(f'{" ":20s}{Arg31:d}')

    sutx1.group=gid
    sutx2.group=gid
    sutx3.group=gid
    sGroup=[sutx2,sutx3,sutx1]
    write_to_file(sGroup,"TX/group.stx")
    print("writing signed transactions in TX/group.stx")

    print(f'{"Sending transaction"}')
    txId=algodClient.send_transactions(sGroup)
    print(f'{"Transaction id:":20s}{txId:s}')
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)

    main(MnemFile,index,algodClient)
    
