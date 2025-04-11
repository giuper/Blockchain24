import sys
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn, write_to_file,calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from utilityAsset import print_asset_holding

TXFolder="TX/"

def swap(account1,account2,assetId,algodClient):

    params=algodClient.suggested_params()

    sk1,pk1=getSKAddr(account1)
    sk2,pk2=getSKAddr(account2)

##account1 transfers 4 unit of the asset to account2 
    txn1=AssetTransferTxn(
        sender=pk1,sp=params,receiver=pk2,amt=4,index=assetId)
    write_to_file([txn1],TXFolder+"A1toA2.utx")

##account2 pays account1 1Algo 
    txn2=PaymentTxn(
        sender=pk2,sp=params,receiver=pk1,amt=10_000_000)
    write_to_file([txn2],TXFolder+"A2toA1.utx")

##create the group
    gid=calculate_group_id([txn1, txn2])

#account 1 signs the asset transfer
    txn1.group=gid
    write_to_file([txn1],TXFolder+"A1toA2withGID.utx")
    stxn1=txn1.sign(sk1)
    write_to_file([stxn1],TXFolder+"A1toA2withGID.stx")

#account2 signs the payment transaction txn2
    txn2.group=gid
    write_to_file([txn2],TXFolder+"A2toA1withGID.utx")
    stxn2=txn2.sign(sk2)
    write_to_file([stxn2],TXFolder+"A2toA1withGID.stx")

    print("Asset holding before the transaction")
    print(f'{"Account 1:":28s}{pk1:s}')
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print(f'{"Account 2:":28s}{pk2:s}')
    print_asset_holding(algodClient,pk2,assetId)

    signedTL=[stxn1,stxn2]
    txid=algodClient.send_transactions(signedTL)
    print(f'{"Transaction id:":28s}{txid:s}')

    wait_for_confirmation(algodClient,txid,4)

    print()
    print("Asset holding after the transaction")
    print(f'{"Account 1:":28s}{pk1:s}')
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print(f'{"Account 2:":28s}{pk2:s}')
    print_asset_holding(algodClient,pk2,assetId)


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <account1 sending asset> <account2 sending algo> <assetId>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    assetId=int(sys.argv[3])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    swap(account1,account2,assetId,algodClient)
