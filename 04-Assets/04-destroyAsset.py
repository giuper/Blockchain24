import sys
import json
from algosdk import error
from algosdk.v2client import algod
from algosdk.future import transaction 
from algosdk.future.transaction import AssetConfigTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from localUt import TXFolder

def destroyAsset(managerMNEMFile,assetID,algodClient):

    params=algodClient.suggested_params()
    managerSK,managerADDR=getSKAddr(managerMNEMFile)

    txn=AssetConfigTxn(sender=managerADDR,
                       sp=params,
                       index=assetID,
                       strict_empty_address_check=False)
    transaction.write_to_file([txn],TXFolder+"04-assetDestroy.utxn")
    stxn=txn.sign(managerSK)
    txid=algodClient.send_transaction(stxn)
    print(f'{"TX id:":32s}{txid:s}')
    transaction.write_to_file([stxn],TXFolder+"04-assetDestroy.stxn")

    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

    return 
    

if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python",sys.argv[0],"<manager MNEM file> <asset ID>")
        exit()

    managerMNEMFile=sys.argv[1]
    assetID=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    destroyAsset(managerMNEMFile,assetID,algodClient)

