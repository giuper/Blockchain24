import sys
import json
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, write_to_file
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from localUt import TXFolder

def optin(holderMNEMFile,assetID,algodClient):

    params=algodClient.suggested_params()
    holderSK,holderAddr=getSKAddr(holderMNEMFile)

    #check if account has already opted in
    accountInfo=algodClient.account_info(holderAddr)
    holding=False
    print(f'{"User Addr:":32s}{holderAddr:s}')
    for asset in accountInfo['assets']:
        if (asset['asset-id']==assetID):
            holding = True
            print(f'{"":32s}{"Already opted in":s}')
            break

    if holding:
        return

    txn=AssetTransferTxn(sender=holderAddr,sp=params,receiver=holderAddr,amt=0,index=assetID,close_assets_to=holderAddr)
    write_to_file([txn],TXFolder+"05-assetOPTout.utxn")

    stxn=txn.sign(holderSK)
    write_to_file([stxn],TXFolder+"05-assetOPTout.stxn")


    txid=algodClient.send_transaction(stxn)
    print(f'{"TX id:":32s}{txid:s}')
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))


if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python",sys.argv[0],"<holder MNEM file> <assetID>")
        exit()

    holderMNEMFile=sys.argv[1]
    assetID=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    
    optin(holderMNEMFile,assetID,algodClient)

