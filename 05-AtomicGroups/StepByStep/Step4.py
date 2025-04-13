import sys
from algosdk.v2client import algod
from algosdk.future.transaction import retrieve_from_file
from utilities import algodToken, algodAddress, wait_for_confirmation

def sendGroup(ftx1,ftx2,algodClient):

    params=algodClient.suggested_params()

    tx1=retrieve_from_file(ftx1)
    tx2=retrieve_from_file(ftx2)
    
    signedTL=[tx1[0],tx2[0]]
    txid=algodClient.send_transactions(signedTL)
    print(f'{"Transaction id:":28s}{txid:s}')

    wait_for_confirmation(algodClient,txid,4)


if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python "+sys.argv[0]+" <file with transaction 1> <file with transaction 2>")
        exit()

    ftx1=sys.argv[1]
    ftx2=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    sendGroup(ftx1,ftx2,algodClient)
