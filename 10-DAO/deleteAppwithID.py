import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationDeleteTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e

def deleteApp(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    print("User addr:",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:   ",appId)
    print("App addr: ",appAddr)
    
    utxn=ApplicationDeleteTxn(sender=Addr,sp=params,index=appId,foreign_assets=[106902214,106902215,106903591,106903592])
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Tx id:    ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Deleted:  ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    deleteApp(MnemFile,appId,directory)
    
    
