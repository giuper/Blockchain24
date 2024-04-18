import sys
import json
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, write_to_file
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def transfer(senderMNEMFile,receiverADDRFile,assetID,algodClient):
    
    params=algodClient.suggested_params()
    
    senderSK,senderAddr=getSKAddr(senderMNEMFile)

    with open(receiverADDRFile,'r') as f:
        receiverAddr=f.read()

    print(f'{"Sender Addr:":32s}{senderAddr:s}')
    print(f'{"User Addr:":32s}{receiverAddr:s}')
    
    txn=AssetTransferTxn(sender=senderAddr,sp=params,
                receiver=receiverAddr,amt=1000,index=assetID)
    write_to_file([txn],"TX/03-assetTrans.utxn")
    
    stxn=txn.sign(senderSK)
    write_to_file([stxn],"TX/03-assetTrans.stxn")

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
    if (len(sys.argv)!=4):
        print("Usage: python3",sys.argv[0],"<sender MNEM file> <receiver ADDR file> <assetID>")
        exit()
    senderMNEMFile=sys.argv[1]
    receiverADDRFile=sys.argv[2]
    assetID=int(sys.argv[3])
    algodClient=algod.AlgodClient(algodToken,algodAddress)

    transfer(senderMNEMFile,receiverADDRFile,assetID,algodClient)
