import sys
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn, calculate_group_id, retrieve_from_file, write_to_file
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

TXFolder="TX/"

def signT(filet,filem):

    sk,pk=getSKAddr(filem)
    ltxn=retrieve_from_file(filet)
    txn=ltxn[0]
    stxn=txn.sign(sk)
    write_to_file([stxn],TXFolder+"Step3A2.stx")



if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python "+sys.argv[0]+" <file tx> <mnem sending asset>")
        exit()

    filet=sys.argv[1]
    filem=sys.argv[2]
    signT(filet,filem)
