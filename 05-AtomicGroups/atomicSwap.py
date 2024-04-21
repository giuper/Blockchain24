import sys
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn, write_to_file,calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from utilityAsset import print_asset_holding


def swap(account1,account2,assetId,algodClient):

    params=algodClient.suggested_params()

    sk1,pk1=getSKAddr(account1)
    sk2,pk2=getSKAddr(account2)


##account2 pays account1 1Algo 
    txn0=PaymentTxn(
        sender=pk2,sp=params,receiver=pk1,amt=1_000_000)
    write_to_file([txn0],"TX/A2toA1.utx")


##account1 transfers 4 unit of the asset to account2 
    txn1=AssetTransferTxn(
        sender=pk1,sp=params,receiver=pk2,amt=4,index=assetId)
    write_to_file([txn1],"TX/A1toA2.utx")

##create the group
    gid=calculate_group_id([txn0, txn1])

#account2 signs the payment transaction txn0
    txn0.group=gid
    write_to_file([txn0],"TX/A2toA1withGID.utx")
    stxn0=txn0.sign(sk2)
    write_to_file([stxn0],"TX/A2toA1withGID.stx")

#account 1 signs the asset transfer
    txn1.group=gid
    write_to_file([txn1],"TX/A1toA2withGID.utx")
    stxn1=txn1.sign(sk1)
    write_to_file([stxn1],"TX/A1toA2withGID.stx")

    print("Asset holding before the transaction")
    print("Account 1:      ",pk1)
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print("Account 2:      ",pk2)
    print_asset_holding(algodClient,pk2,assetId)

    signedTL=[stxn0,stxn1]
    txid=algodClient.send_transactions(signedTL)
    print("Transaction id: ",txid)

    wait_for_confirmation(algodClient,txid,4)

    print()
    print("Asset holding after the transaction")
    print("Account 1:      ",pk1)
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print("Account 2:      ",pk2)
    print_asset_holding(algodClient,pk2,assetId)


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <account1> <account2> <assetId>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    assetId=int(sys.argv[3])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    swap(account1,account2,assetId,algodClient)
