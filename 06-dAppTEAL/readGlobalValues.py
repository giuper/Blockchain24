import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn
from algosdk.future.transaction import OnComplete
from algosdk.future.transaction import StateSchema
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(AddrFile,index,algodClient):

    with open(AddrFile,'r') as f:
        Addr=f.read()

    print(f'{"User address: ":32s}{Addr:s}')
    print(f'{"Calling in: ":32s}{index:d}')

    print("Reading the global values")
    results=algodClient.account_info(Addr)
    appsCreated=results['created-apps']
    #print("apprsCreated\n",appsCreated)
    for app in appsCreated :
        if app['id']==index :
            #print(f"global_state for app_id {index}: ", app['params']['global-state'])
            for kk in app['params']['global-state']:
                key=kk['key']
                key=base64.b64decode(key)
                key=key.decode('utf-8')
                print(key,kk['value'])


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <addr> <app index>")
        exit()

    AddrFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(AddrFile,index,algodClient)

       
