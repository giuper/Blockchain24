import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, ApplicationClearStateTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):

    params=algodClient.suggested_params()
    SK,Addr=getSKAddr(MnemFile)

    print(f'{"User address: ":32s}{Addr:s}')
    print(f'{"Clearing: ":32s}{index:d}')

    utx=ApplicationClearStateTxn(Addr,params,index)
    write_to_file([utx],"TX/clear.utx")

    stx=utx.sign(SK)
    write_to_file([stx],"TX/clear.stx")

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')
    algodClient.send_transactions([stx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    idfromtx=txResponse['txn']['txn']['apid']
    print(f'{"Cleared app-id: ":32s}{idfromtx:d}')  


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)

    main(MnemFile,index,algodClient)
    
    
