import sys
import base64

from algosdk.future import transaction
from algosdk import mnemonic
from algosdk.v2client import algod
from utilities import algodAddress, algodToken, wait_for_confirmation

    

def createAndSign(myprogramF,argStr,receiverADDRF,amount,algodClient):

    # Read TEAL program
    with open(myprogramF,'r') as f:
        data=f.read()
    
    # Compile TEAL program
    response=algodClient.compile(data)
    sender=response['hash']
    programstr=response['result']
    print(f'{"Response Result":30s}{programstr:s}')
    print(f'{"Response Hash":30s}{sender:s}')
        
    # Create logic sig
    t=programstr.encode()
    program=base64.decodebytes(t)
    

    arg1=argStr.encode()
    lsig=transaction.LogicSig(program, args=[arg1])

    with open(receiverADDRF,'r') as f:
        receiver=f.read()
    closeremainderto=receiver
    params=algodClient.suggested_params()
    txn = transaction.PaymentTxn(
            sender,params,receiver,amount,closeremainderto)
    
    # Create the LogicSigTransaction with contract account LogicSig
    lstx=transaction.LogicSigTransaction(txn,lsig)
    transaction.write_to_file([lstx],"TX/"+sys.argv[0][:-3]+".stx")

    # Send raw LogicSigTransaction to network
    try:
        txid=algodClient.send_transaction(lstx)
        print(f'{"Transaction ID":30s}{txid:s}')
    except Exception as e:
        print(e)
        exit()
    
    wait_for_confirmation(algodClient,txid,4)

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("Usage: ",sys.argv[0],"<receiver ADDR file> <TEAL program file> ")
        exit()
    
    receiverADDRF=sys.argv[1]
    myprogramF=sys.argv[2]

##specify here your argument
##this is the passphrase to unlock passphrase.teal
    argStr="weather comfort erupt verb pet range endorse exhibit tree brush crane man"

    print(f'{"Argument for teal program":30s}{argStr:s}')

    algodClient=algod.AlgodClient(algodToken,algodAddress)
    amount=1_000_000

    createAndSign(myprogramF,argStr,receiverADDRF,amount,algodClient)
