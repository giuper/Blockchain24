import sys
from algosdk import account
from algosdk.v2client import algod
from utilities import algodAddress, algodToken

def listAssets(creatorADDRFile,algodClient):

    with open(creatorADDRFile,'r') as f:
        creatorAddr=f.read()

    print(f'{"Creator Addr:":32s}{creatorAddr:s}')
    accountInfo=algodClient.account_info(creatorAddr)
    #print(accountInfo)
    noca=len(accountInfo['created-assets'])
    if noca==0:
        print(f'{"No asset created"}')
        exit()
    else:
        print(f'{"Number of created assets:":32s}{noca:d}')
    
    for asset in accountInfo['created-assets']:
        print("Index: ",asset['index'])
        print("\t",asset['params']['name'])
        print("\t","Creator: ",asset['params']['creator'])
        print("\t","Manager: ",asset['params']['manager'])
        print()
    return
    

if __name__=="__main__":
    if (len(sys.argv)!=2):
        print("Usage: python",sys.argv[0],"<creator Addr file>")
        exit()

    creatorADDRFile=sys.argv[1]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    listAssets(creatorADDRFile,algodClient)

