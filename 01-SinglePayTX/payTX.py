import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn, write_to_file
from utilities import algodAddress, algodToken, wait_for_confirmation


def payTX(sKey,sAddr,rAddr,amount,algodClient):

    params = algodClient.suggested_params()

    unsignedTx=PaymentTxn(
        sender=sAddr,
        sp=params,
        receiver=rAddr,
        amt=amount,
        note=b"Ciao Pino",
    )
    write_to_file([unsignedTx],"TX/Pay.utx")

    signedTx=unsignedTx.sign(sKey)
    write_to_file([signedTx],"TX/Pay.stx")

    txid=algodClient.send_transaction(signedTx)
    print(f'{"Signed transaction with txID:":32s}{txid:s}')
    print()

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    account_info = algodClient.account_info(sAddr)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


def main():
    if len(sys.argv)!=3:
        print("usage: "+sys.argv[0]+" <file with sender key> <file with receiver addr>")
        exit()

    amount=1_000_000

    algodClient = algod.AlgodClient(algodToken,algodAddress)

    senderKeyF=sys.argv[1]
    with open(senderKeyF,'r') as f:
        passphrase=f.read()
    sKey=mnemonic.to_private_key(passphrase)
    sAddr=mnemonic.to_public_key(passphrase)
    print(f'{"Sender address:":32s}{sAddr:s}')
    account_info = algodClient.account_info(sAddr)
    balance=account_info.get('amount')
    print(f'{"Account balance:":32s}{balance:d}{" microAlgos"}')

    receiverAddrF=sys.argv[2]
    with open(receiverAddrF,'r') as f:
        rAddr=f.read()
    print(f'{"*Receiver address:":32s}{rAddr:s}')

    if (amount<=balance):
        payTX(sKey,sAddr,rAddr,amount,algodClient)
    else:
        print("Insufficient funds")

if __name__=='__main__':
    main()
