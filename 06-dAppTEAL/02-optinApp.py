import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationOptInTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):

    print(f'{"Opting in: ":32s}{index:d}')

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    print(f'{"User address: ":32s}{Addr:s}')

    params=algodClient.suggested_params()
    utx=ApplicationOptInTxn(Addr,params,index)
    write_to_file([utx],"TX/optin.utx")

    stx=utx.sign(SK)
    write_to_file([stx],"TX/optin.stx")

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')

    algodClient.send_transactions([stx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    idfromtx=txResponse['txn']['txn']['apid']
    print(f'{"OptIn to app-id: ":32s}{idfromtx:d}')  


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(MnemFile,index,algodClient)
    
    
