# *Blockchain*
## UNISA Spring 25 ##

## Using Ed25519 in contracts

In this unit we show how to make a smart contract that verifies an
Ed25519 signature. 
Check [this](./ExploringKeys.md) file for a discussion of how Ed25519 keys are used and encoded in Algorand.

### The contract in TEAL
The contract has success only if it receives as first argument the signature of the string `goAlgorand` that passes the verification with respect to the address `MP75KSDYVIFBBJAHCBQEEI57RGNSS6DDZZFUEC5DUW6VNUDOA2KEDOHJJM`.
The relevant TEAL fragment is the following

```
verify:
byte base64(Z29BbGdvcmFuZA==)
txn ApplicationArgs 0
addr MP75KSDYVIFBBJAHCBQEEI57RGNSS6DDZZFUEC5DUW6VNUDOA2KEDOHJJM
ed25519verify
return
```
Here, `Z29BbGdvcmFuZA==` is the base-64 encoding of the string `goAlgorand`.

The `ed25519verify` instruction exceeds (1900) the budget of a single transaction (700) and therefore we must submit a group of three transactions. Each transaction of the group has two arguments: the TEAL contract accepts all transactions whose second argument is 0; 
if the second argument is non-zero, it branches to `verify`  to check if the first argument is a valid signature (see above). Keep in mind that this is just a domonstration and that if we pass one transaction with second argument 0 and no signature at all, the contract is satisfied. 
The relevant TEAL fragment is the following.
```
txn ApplicationArgs 1
btoi
bnz verify
int 1
return 
```
Note that the two dummy transactions must be different and one way to differentiate them is to pass a different first argument. The first argument of the non-dummy transaction is of course the signature.

The script `03-callApp.py` constructs the group of three transactions (two dummy and one with the signature) and calls the contract. The signature is hardcoded in the program in base64 format but it must be passed decoded to the contract. 
In the next two paragraph below we explain how to extract the secret key from the mnemonic (see the file [secretkey.py](./secretkey.py) ) and how to sign a string (see the file [signFromMnem.py](signFromMnem.py) ).


### Extracting secret/public key from the mnemonic
We assume to have a mnemonic stored in file ```account.mnem``` and
wish to extract the secret+public key to be used to sign in file ```account.skk```

The method ```mnemonic.to_private_key``` constructs the secret key from the mnemonic.
This is the base64 encoding of the pair *(sk,pk)* where each component is 32byte.
*sk* is the randomness used to generate the point *A* that constitutes the *pk*.
Specifically, *H(sk)=(s,k)* and *A=sB*, where *B* is a publicly known point on the curve.

Python program ```publickey.py``` reads the mnemonic from a mnem file and outputs the public key
computed in two different ways: by splitting the secret key and returning the second half, 
and by using the first half of the secret key as a random seed to obtain the public key with
the *publickey* method of the pythong implementation of the Ed25519.

Python program ```secretkey.py``` reads the mnemonic from 
```account.mnem``` and uses ```mnemonic.to_private_key``` that returns
the secret key in base64 encoding.  Then it decodes it and writes it in
```account.skk```. The encoded private key is stored in ```account.sk64```.

A similar effect can be obtained by using the command

```~/node/algokey import -m <mnem> --keyfile <fileforsecretkey>```

where ```<mnem>``` is the 25-word mnemonic (not the name of the file containing it).

Note that the two secret keys extracted differ but they produce the same signature.
<Discussion to be added>


### Signing using the secret key
Once we have the secret key we can proceed to sign the data.
To avoid signature replay attacks, we apply domain separation and thus the actual data that the ```ed25519verify`` opcode expects is 
a 64 byte signature of the string “ProgData” concatenated with the hash of the program and the data that was signed (see [this](https://developer.algorand.org/articles/verify-signatures-and-signed-data-within-algorand-smart-contracts/)). 
The signature can be obtained with the following command:

```goal clerk tealsign --data-b64 <data B64 encoded>  --contract-addr <hash of teal file> --keyfile <secret key file>```

### Signing from python
[This](./signFromMnem.py) script takes on the command line a file containing a mnemonic (without the .mnem extension), the name of file containing a TEAL compiled program (without the .tok extension) the string to be signed, and, alternatively to the tok file, the encoded hash of the TEAL program.
It uses the implementation of the EdDSA signature scheme over Curve25519 found at [https://github.com/pyca/ed25519](https://github.com/pyca/ed25519).
The script performs the following operations:

1. Goes from mnemonic to base64 encoded private key using the ```mnemonic.to_private_key``` from the SDK and then obtaine the private key by b64decoding the string obtained. This results in 64 bytes, the first 32 bytes are the secret key and the remaining are the public key.
2. The public key is derived also from the secret key by applying the ```publickey``` method from the python implementation in ed25519.
3. The hash of the program is computed in two different ways: 
    1. from the encoded hash of the program (hard-coded in the script). 
The encoded hash is obtained as an output by the compiling command ```goal clerk compile``` that produces the bytecode file.  Alternatively, as the ```hash``` field of the dict returned by the ```compile``` method of the  ```algod.AlgodClient``` class executed on the TEAL source file.  Note that the ```compile``` method returns the bytecode in the ```result``` field.  The actual hash is obtained by appending the appropriate number of `=` characters and then by base32 decoding the encoded hash.
    2. or by reading the bytecode, prepending the string ```Program``` to it for domain separation and then by hashing it with SHA512/256. The value obtained is then hashed again and the last 4 bytes are appended as a checksum
to obtain the final value.
The string "Program" is used for hash domain separation.
4. Finally the signature is computed by signing the concatenation of the string "ProgData" (for domain separation), the unmarshaled (i.e., without the 4 byte checksym) hash of the byte code and the actual string to be signed.

### References
[This](https://developer.algorand.org/articles/verify-signatures-and-signed-data-within-algorand-smart-contracts/) article is very useful.

[This](https://developer.algorand.org/docs/get-details/dapps/avm/teal/opcodes/v10/) web page lists the cost of all TEAL opcodes.
