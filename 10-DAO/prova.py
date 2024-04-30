import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e
from daoutilities import getAssetFromAddr,getAllAssets, assetInfo

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <addr> <node directory>")
        exit()
    addrFile=sys.argv[1]
    directory=sys.argv[2]
    with open(addrFile,'r') as f:
        Addr=f.read()
    algodClient=getClient(directory)
    LL=getAllAssets(Addr,algodClient)
    for ll in LL:
        assetInfo(ll,algodClient)


