import sys
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from algosdk.future.transaction import AssetConfigTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from localUt import AssetName, AssetUnit

def createAsset(AssetName,creatorMNEMFile,managerADDRFile,algodClient):
    
    params=algodClient.suggested_params()
    creatorSK,creatorAddr=getSKAddr(creatorMNEMFile)
    
    with open(managerADDRFile,'r') as f:
        managerAddr=f.read()
    reserveAddr=managerAddr
    freezeAddr=managerAddr
    clawbackAddr=managerAddr
    
    print(f'{"Creator Addr:":32s}{creatorAddr:s}')
    print(f'{"Manager Addr:":32s}{managerAddr:s}')
    print(f'{"Reserve Addr:":32s}{reserveAddr:s}')
    print(f'{"Freeze  Addr:":32s}{freezeAddr:s}') 
    print(f'{"ClawbackAddr: ":32s}{clawbackAddr:s}')

    txn=AssetConfigTxn(
        sender=creatorAddr,
        sp=params,
        total=1000,
        default_frozen=False,
        asset_name=AssetName,
        unit_name=AssetUnit,
        manager=managerAddr,
        reserve=reserveAddr,
        freeze=freezeAddr,
        clawback=clawbackAddr,
        url="https://github.com/giuper/Blockchain24",
        decimals=0)

    transaction.write_to_file([txn],TXFolder+"01-assetCreation.utxn")
    stxn=txn.sign(creatorSK)
    transaction.write_to_file([stxn],TXFolder+"01-assetCreation.stxn")

    txid=algodClient.send_transaction(stxn)
    print(f'{"TX id:":32s}{txid:s}')
    
    confirmed_txn=wait_for_confirmation(algodClient,txid,4)
    try:
        ptx=algodClient.pending_transaction_info(txid)
        assetId=ptx["asset-index"]
        print(f'{"Created an asset with id:":32s}{assetId:d}')
    except Exception as e:
        print(e)
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn,indent=4)))

    exit()


if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python3",sys.argv[0],"<creator MNEM file> <manager ADDR>")
        exit()

    creatorMNEMFile=sys.argv[1]
    managerADDRFile=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    createAsset(AssetName,creatorMNEMFile,managerADDRFile,algodClient)
