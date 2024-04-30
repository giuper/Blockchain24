import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn, AssetTransferTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e

def getSellingPrice(creatorAddr,appIndex,algodClient):
    app=algodClient.application_info(appIndex)
    for kk in app['params']['global-state']:
        key=kk['key']
        key=base64.b64decode(key)
        key=key.decode('utf-8')
        if key=="scurrentPrice":
            return kk['value']['uint']

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <creator> <app index> <node directory>")
        exit()

    creatorFile=sys.argv[1]
    with open(creatorFile,"r") as f:
        creatorAddr=f.read()
    appIndex=int(sys.argv[2])
    directory=sys.argv[3]
    algodClient=getClient(directory)
    print(getSellingPrice(creatorAddr,appIndex,algodClient)+3)
    

