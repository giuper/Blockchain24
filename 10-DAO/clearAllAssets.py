import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetCloseOutTxn, AssetDestroyTxn
from algosdk.future import transaction
from utilities import wait_for_confirmation, getClient
from daoutilities import getAllAssets, getAssetCreator, getAmountAssetFromAddrIndex

def removeAllAssets(MnemFile,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)

    listAssets=getAllAssets(Addr,algodClient)
    print(f'Found {len(listAssets)} assets for address {Addr}')

    for index in listAssets:
        creator=getAssetCreator(index,algodClient)
        if creator is None:
            print(f'Asset {index} non-existing')
            continue

        print(f'Removing asset {index} created by {creator:s}')
        if creator!=Addr:
            utxn=AssetCloseOutTxn(sender=Addr,sp=params,receiver=creator,index=index)
        else:
            if algodClient.asset_info(index)['params']['total']==getAmountAssetFromAddrIndex(Addr,index,algodClient):
                print(f'\tCreator holding all assets')
                utxn=AssetDestroyTxn(sender=Addr,sp=params,index=index)
            else:
                print(f'\tCreator not holding all assets')
                continue
        stxn=utxn.sign(SK)
        txId=algodClient.send_transaction(stxn)
        try:
            confirmed_txn=wait_for_confirmation(algodClient,txId,4)  
        except Exception as err:
            print(f'Error in {txId}')
            continue
        print(txId)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python "+sys.argv[0]+" <mnem> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    directory=sys.argv[2]
    removeAllAssets(MnemFile,directory)
