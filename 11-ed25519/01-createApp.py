#!/usr/bin/python3.10

import sys
import json
import base64
from algosdk import account, mnemonic
import algosdk.encoding as e
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, ApplicationCreateTxn, OnComplete, StateSchema
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

tealApproval="TEAL/edCompact.teal"
tealClear="TEAL/clear.teal"

def main(creatorMnemFile,algodClient):

    creatorSK,creatorAddr=getSKAddr(creatorMnemFile)
    print(f'{"Creator address: ":32s}{creatorAddr:s}')

    print(f'{"Reading clear file:":32s}{tealClear:s}')
    with open(tealClear,'r') as f:
        clearProgramSource=f.read()
    print(f'{"Compiling the clear program"}')
    compile_response=algodClient.compile(clearProgramSource)
    clearProgram=base64.b64decode(compile_response["result"])
    
    print(f'{"Reading approval file:":32s}{tealApproval:s}')
    with open(tealApproval,'r') as f:
        approvalProgramSource=f.read()
    print(f'{"Compiling approval file"}')
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])
    print(f'{"App Hash:":32s}{approvalProgramResponse["hash"]}')
    exit()

    # declare application state storage (immutable)
    # no need for global storage
    global_ints=0
    global_bytes=0
    globalSchema=StateSchema(global_ints,global_bytes)

    # no need for local storage
    local_ints=0
    local_bytes=0
    localSchema=StateSchema(local_ints,local_bytes)


    params=algodClient.suggested_params()

    utx=ApplicationCreateTxn(
        creatorAddr,
        params,
        OnComplete.NoOpOC,
        approval_program=approvalProgram,
        clear_program=clearProgram,
        global_schema=globalSchema,
        local_schema=localSchema,
    )
    write_to_file([utx],"TX/create.utx")


    stx=utx.sign(creatorSK)
    write_to_file([stx],"TX/create.stx")

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')
    txId=algodClient.send_transactions([stx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print(json.dumps(txResponse,indent=2))

    appId=txResponse['application-index']
    print(f'{"App id:":32s}{appId:d}');
    appaddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    print(f'{"App address:":32s}{appaddr:32}')
    print(f'{"App Hash:":32s}{approvalProgramResponse["hash"]}')

if __name__=='__main__':
    if len(sys.argv)!=2:
        print("usage: python3 "+sys.argv[0]+" <creator mnem file>")
        exit()

    creatorMnemFile=sys.argv[1]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(creatorMnemFile,algodClient)

