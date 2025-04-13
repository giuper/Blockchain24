import sys
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn, retrieve_from_file, write_to_file, calculate_group_id
from utilities import getSKAddr

TXFolder="TX/"

def cgid(file1,file2,filem):

    sk1,pk1=getSKAddr(filem)
    ltxn1=retrieve_from_file(file1)
    txn1=ltxn1[0]
    ltxn2=retrieve_from_file(file2)
    txn2=ltxn2[0]
    gid=calculate_group_id([txn1,txn2])
    txn1.group=gid
    txn2.group=gid
    write_to_file([txn1],TXFolder+"Step2A1.utx")
    write_to_file([txn2],TXFolder+"Step2A2.utx")

    stxn1=txn1.sign(sk1)
    write_to_file([stxn1],TXFolder+"Step2A1.stx")



if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <file tx1> <file tx2> <mnem sending asset>")
        exit()

    filetx1=sys.argv[1]
    filetx2=sys.argv[2]
    filem=sys.argv[3]
    cgid(filetx1,filetx2,filem)
