import sys
import base64
#from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, ApplicationNoOpTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):


    params=algodClient.suggested_params()
    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address: ":32s}{Addr:s}')
    print(f'{"Calling in: ":32s}{index:d}')

    utx=ApplicationNoOpTxn(Addr,params,index)
    write_to_file([utx],"TX/noop.utx")

    stx=utx.sign(SK)
    write_to_file([stx],"TX/noop.stx")

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')
    algodClient.send_transactions([stx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    idfromtx=txResponse['txn']['txn']['apid']
    print(f'{"Calling app-id: ":32s}{idfromtx:d}')  

    print("Global values from the TX output")
    if "global-state-delta" in txResponse:
        #print(txResponse['global-state-delta'])
        for variable in txResponse['global-state-delta']:
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("\tGlobal Key: ",key)
            #print(variable)
            if 'uint' in variable['value']:
                print("\tValue     : ",variable['value']['uint'])
            else:
                print("\tValue     : 0")

    print("Local values from the TX output")
    if "local-state-delta" in txResponse :
        #print(txResponse['local-state-delta'])
        for variable in txResponse['local-state-delta'][0]['delta']:
            #key=txResponse['local-state-delta'][0]['delta'][0]['key']
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("\tLocal Key : ",key)
            if 'uint' in variable['value']:
                print("\tValue     : ",variable['value']['uint'])
            else:
                print("\tValue did not change")

    print("Local values from account_info")
    result=algodClient.account_info(Addr)
    localState=result['apps-local-state']
    for st in localState:
        if(st['id']==index):
            for kk in st['key-value']:
                key=kk['key']
                key=base64.b64decode(key)
                key=key.decode('utf-8')
                print("\tKey    : ",key)
                print("\tValue  : ",kk['value']['uint'])
        

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)

    main(MnemFile,index,algodClient)
    
    
