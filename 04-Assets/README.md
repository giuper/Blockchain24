# *Blockchain*
## UNISA Spring 24 ##

## Algorand Standard Assets (ASAs) ##

### Step by step  ###

1. Run [01-createAsset.py](./01-createAsset.py) to create asset with name ```DISAMIS24```.
It takes two command line arguments: 
the filename containing the mnemonic of the creator account and
the filename containing the address of the manager.
Take note of the asset index that will be needed for the following steps.

```python
    txn=AssetConfigTxn(
        sender=creatorAddr,
        sp=params,
        total=1000,
        default_frozen=False,
        asset_name=AssetName,
        unit_name=AssetUnit,
        manager=managerAddr,
        reserve=reserveAddr,
        freeze=freezeAddr,
        clawback=clawbackAddr,
        url="https://github.com/giuper/Blockchain24",
        decimals=0)
```

The script sets the ```reserve address```, ```freeze address```, and ```clawback address``` equal to
the ```manager address```. 


The unsigned and signed transaction are found in files ```assetCreation.utxn``` and 
```assetCreation.stxn```, respectively. 
Use ```goal clerk inspect``` to view their content.

2. [listCreatedAsset.py](./listCreatedAsset.py) can be used to list all assets created by an address.
    It takes one command line argument: the filename containing the address of the creator.

    Just need to know where to look in the dict returned by ```account_info```

```python

    accountInfo=algodClient.account_info(creatorADDR)
    for asset in accountInfo['created-assets']:
        print("Index: ",asset['index'])
        print("\t",asset['params']['name'])
        print("\t","Creator: ",asset['params']['creator'])
        print("\t","Manager: ",asset['params']['manager'])
        print()
```

3. Run [02-optinAsset.py](./02-optinAsset.py) to allow addresses to opt in the asset.
    It takes two command line arguments: 
    the filename containing the mnemonic of the address that wishes to opt in and the asset index.
   
    The transaction is just a transfer with 0 amount to myself.

```python
    txn=AssetTransferTxn(sender=holderAddr,
            sp=params,receiver=holderAddr,amt=0,index=assetID)
```
    
The unsigned and signed transaction are found in files ```assetOPTin.utxn``` and 
```assetOPTin.stxn```, respectively. 
Use ```goal clerk inspect``` to view their content.

4. Run [03-transferAsset.py](./03-transferAsset.py) to transfer assets between two addresses. 
    It takes two command line arguments: 
    the filename containing the mnemonic of the sender,
    the filename containing the address of the receiver,
    the asset index.

    The transaction is what you would expect from the previous one.

```python
    txn=AssetTransferTxn(sender=senderAddr,sp=params,
                receiver=receiverAddr,amt=10,index=assetID)
```

The unsigned and signed transaction are found in files ```assetTrans.utxn``` and 
    ```assetTrans.stxn```, respectively. 
    Use ```goal clerk inspect``` to view their content.

5. Run [04-destroyAsset.py](./04-destroyAsset.py) to destroy an asset.
    Note that it is required that, at the time an asset is destroy, all instances
    of the asset are owned by the manager.
