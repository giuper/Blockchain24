# *Blockchain*
## UNISA Spring 25 ##

## Using ed25519 in contracts

In this unit we show how to make a smart contract that verifies an
ed25519 signature.

### Extracting the secret key from the mnemonic
We assume to have a mnemonic stored in file ```account.mnem``` and
wish to extract the secret key to be used to sign in file ```account.skk```

Python program ```secretkey.py``` reads the mnemonic from 
```account.mnem``` and uses ```mnemonic.to_private_key``` that returns
the secret key in base64 encoding.  Then it decodes it and writes it in
```account.skk``. The encoded private key is stored in ```account.sk64```.

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



### References
[This](https://developer.algorand.org/articles/verify-signatures-and-signed-data-within-algorand-smart-contracts/) article is very useful.
