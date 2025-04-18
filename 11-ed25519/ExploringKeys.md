# *Blockchain*
## UNISA Spring 25 ##

## Exploring keys in Algorand

Algorand uses the Ed25519 signature scheme to sign transactions and an Algorand address is 
essentially an Ed25519 verification (aka public) key.
In this unit we explore the way public and secret key (that is, verification and signing keys) can
be extracted from the mnem file and from an Algorand address.
The primary reference is the [Ed25519 web site](https://ed25519.cr.yp.to/).

### The curve and the points

The signature scheme uses the twisted Edwards form of an elliptic curve in Montogomery form.
Specifically we start from elliptic curve in Montgomery form

$$Bv^2=u^3+Au^2+u$$

with $A\ne\pm 2$ and $B\ne 0$ and we obtain the twisted Edwards form 

$$ax^2+y^2=1+dx^2y^2$$

with $a,d\ne 0$ and $a\ne d$ by applying the map

$$(u,v)\rightarrow (x,y)=\left(\frac{u}{v},\frac{u-1}{u+1}\right)$$

which sets $a=(A+2)/B$ and $d=(A-2)/B$.

In Ed25519 we set $B=1$ and $A=48662$ over the field modulo the prime $q=2^{255}-19$.
which in twisted Edwards form becomes

$$-x^2+y^2=1-\frac{121665}{121666} x^2y^2.$$

A point $(x,y)$ over the Edwards curve is represented in extended coordinates
$(X,Y,Z,T)$ such that


$$x=\frac{X}{Z}\quad y=\frac{Y}{Z}\quad x\cdot y=\frac{T}{Z}.$$

The secret key *sk* is a 256-bit random value.
By using *sk* with SHA512 we obtain two 256-bit values *(s,k)=SHA512(sk)*. 
The public key is the point *sB*, where *B* is the base point.
The value *k* is used in computing the signature of a message.


### Extracting secret/public key from the mnemonic
We assume to have a mnemonic stored in file ```account.mnem```.
The method ```mnemonic.to_private_key``` constructs the 
base64 encoding of the pair *(sk,pk)* where each component is 256-bit long.
*sk* is the randomness used to generate the point *A* that constitutes the *pk*.
Specifically, *H(sk)=(s,k)* and *A=sB*, where *B* is a publicly known point on the curve.

Python program ```ed25519keys.py``` reads the mnemonic from a mnem file and performs the following:
    1. obtains *SK64enc* from ```mnemonic.to_private_key''' 
    2. decodes *sK64enc* base64 to obtain *SK64* and sets *sk=SK64[:32]* and *pk=SK64[32:]*
    3. *sk* is the private key and *pk* is the *encoded* point of the public key (see later)
    4. obtains the integer *s* from the first 256 bits of *SHA512(sk)*
    5. obtains point *PS* by multiplying the Ed25519 base point *B* by *s*
    4. the four components of *B* and of *PS* are printed

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
[This](./signFromMnem.py) script takes on the command line a file containing a mnemonic (without the .mnem extension), a TEAL compiled program (without the .tok extension) and the string to be signed. It uses the implementation of the EdDSA signature scheme over Curve25519 found at [https://github.com/pyca/ed25519](https://github.com/pyca/ed25519).
The script performs the following operations:

1. Goes from mnemonic to base64 encoded private key using the ```mnemonic.to_private_key``` from the SDK and then obtaines the private key by b64decoding the string obtained. This results in 64 bytes, the first 32 bytes are the secret key and the remaining are the public key.
2. The public key is derived also from the secret key by applying the ```publickey``` method from the python implementation in Ed25519.
3. The hash of the program is computed in two different ways: from the address of the program (now it is hard-coded in the script) or by reading the bytecode and by hashing it. The string "Program" is used for has domain separation.
4. Finally the signature is computed by signing the concatenation of the string "ProgData" (for domain separation), the unmarshaled (i.e., without the 4 byte checksym) hash of the byte code and the actual string to be signed.

### References
[This](https://developer.algorand.org/articles/verify-signatures-and-signed-data-within-algorand-smart-contracts/) article is very useful.

[This](https://developer.algorand.org/docs/get-details/dapps/avm/teal/opcodes/v10/) web page lists the cost of all TEAL opcodes.
