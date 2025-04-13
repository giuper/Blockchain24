# *Blockchain*
## UNISA Spring 24 (revised in 25) ##

## Transaction groups ##

Algorand supports *groups* of transactions  that are *atomic* in the sense that either all transactions of the group are accepted or none is.

To create a group of transactions from a list of transactions ``ListTX``, first obtain the group id:

```python
    gid=transaction.calculate_group_id(ListTX)
```
then, add the group id to each transaction

```python
    txn.group=gid
```
and finally sign each transaction. Transaction could be signed by a single key, by multiple keys or
logically. The transactions need not to be signed by the same address but need to be submitted 
together
```python
    txid=algodClient.send_transactions(signedListTX)
```


### Step by step  ###
Next we discuss an example in which we construct and submitted 
an atomic group of two transactions:

1. Account1 sends 10 Algos to Account2
2. Account2 sends 4 instances of an ASA to Account1

Script [atomicSwap.py](./atomicSwap.py) takes as input two account addresses and an asset id, and 
submits the group of transactions.

In [folder](./StepByStep) the steps needed to submit a group are implemented in independent scripts.

1. In the [first step of Account1](./StepByStep/Step1-A1.py), Account1 creates a payment transaction for 10 Algo to Account2.
2. In the [first step of Account2](./StepByStep/Step1-A2.py), Account2 creates an asset transfer transaction for 4 coints to Account1 and sends the transaction to Account1.
3. In the [second step by Account1](./StepByStep/Step2.py), Account1 computes the group id of the two transactions computed by the previous two steps, adds to its transactions and signs it. The group id is sent to Account2.
4. In the [third step by Account2](./StepByStep/Step3.py), Account2 adds the group id to its transaction, signs it and sends to Account1.
5. In the [fourth step Account1](./StepByStep/Step4.py), Account1 submits the two signed transactions.

