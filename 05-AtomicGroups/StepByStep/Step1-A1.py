import sys
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn, write_to_file,calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from utilityAsset import print_asset_holding

TXFolder="TX/"

def step1(pk1,pk2,algodClient):

    params=algodClient.suggested_params()
##account2 pays account1 1Algo 
    txn1=AssetTransferTxn(
        sender=pk1,sp=params,receiver=pk2,amt=4,index=assetId)
    write_to_file([txn2],TXFolder+"step1A1.utx")

if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python3.10 "+sys.argv[0]+" <addr1 sending asset> <addr2 sending algo>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    step1(account1,account2)
