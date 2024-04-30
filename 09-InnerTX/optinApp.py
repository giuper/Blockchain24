import sys
import base64
import algosdk.encoding as e
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import ApplicationOptInTxn, PaymentTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):

    params=algodClient.suggested_params()

    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
    print("app id:          ",index)
    print("app Addr:        ",appAddr)

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    playerAddr=account.address_from_private_key(SK)
    print(f'{"User address: ":32s}{playerAddr:s}')

    note="Opt in fee"
    payTx=PaymentTxn(playerAddr,params,appAddr,500_000,None,note)
    optTx=ApplicationOptInTxn(playerAddr,params,index)

    gid=transaction.calculate_group_id([payTx, optTx])
    payTx.group=gid
    optTx.group=gid

    sPayTx=payTx.sign(SK)
    sOptTx=optTx.sign(SK)


    txId=algodClient.send_transactions([sPayTx,sOptTx])
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
    
    
