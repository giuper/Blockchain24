from algosdk.v2client import algod
from algosdk import mnemonic, account
import json

algodToken='' # free service does not require tokens
algodAddress='https://mainnet-api.4160.nodely.dev'
algodAddress='https://testnet-api.4160.nodely.dev:443'
algodAddress='https://testnet-api.4160.nodely.dev'
algodAddress='https://testnet-api.algonode.cloud'

def getSKAddr(MnemFile):
    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    return [SK,Addr]

# utility function for waiting on a transaction confirmation
def wait_for_confirmation(client,transaction_id,timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    cs=client.status()
    start_round=cs["last-round"] + 1
    current_round=start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

