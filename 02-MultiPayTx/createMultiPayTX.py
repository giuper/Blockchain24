import sys
from algosdk import account
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn
from algosdk.future.transaction import write_to_file
from utilities import algodAddress, algodToken


def unsignedMultiSigTX(amount,threshold,version,algodClient,senders,receiver,txFileName):
    
    mSig=Multisig(version,threshold,senders)
    mSigAddr=mSig.address()
    print(f'{"Multisig Address: ":22s}{mSigAddr:s}')

    account_info=algodClient.account_info(mSigAddr)
    balance=account_info.get('amount')
    print(f'{"Account balance:":22s}{balance:d}{" microAlgos"}')
    if balance<amount:
        print("Insufficient funds")
        exit()

    params=algodClient.suggested_params()
    note="Ciao MultiPino!!!".encode()

    unsignedTx=PaymentTxn(mSigAddr,params,receiver,amount,None,note)
    mTx=MultisigTransaction(unsignedTx,mSig)
    write_to_file([mTx],txFileName)
    print("Unsigned transaction in",txFileName)


if __name__=='__main__':
    if len(sys.argv)<4:
        print("usage: python "+sys.argv[0]+" <Addr1> <Addr2> <Addr3> <AddrRec>")
        exit()

    algodClient = algod.AlgodClient(algodToken,algodAddress)

    amount=1_000_000
    version=1
    threshold=2

    senders=[]
    for filename in sys.argv[1:4]:
        with open(filename,'r') as f:
            account=f.read()
        senders.append(account)

    receiverFile=sys.argv[4]
    with open(receiverFile,'r') as f:
        receiver=f.read()

    txFileName="TX/MultiPayWithPK.utx"

    unsignedMultiSigTX(amount,threshold,version,algodClient,senders,receiver,txFileName)
