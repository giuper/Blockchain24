# *Blockchain*
## UNISA Spring 25 ##

## Compact Ed25519 Multi Signature

Following up on the [simple contract](../TEAL/ed25519.teal) that 
verifies an Ed25519 signature, we extend our approach to multi signatures.
Specifically, we would like to have a smart contract that succeeds if an
appropriate signature of a fixed (and known) message is provided for a
list of fixed (and known) Algorand addresses. 
This can be easily achieved in a variety of ways, the simplest being
a contract that performs one check for each Algorand addresses
and succeeds if and only if all checks are successful.
This approach requires a budget that is proportional to the 
number of addresses. 
In this unit, we develop an approach that has a cost that is independent
of the number of addresses.  We start by reviewing how Ed25519 signatures
are computed.

## Ed25519 Signatures

1. **Key Generation**
The secret (signing) key *sk* for Ed25519 is a 256-bit random value 
and the public (verification key *pk* is a multiple of the base point *B*.
The 256 bits of *sk* are expanded into two 256-bit valyes *s* and *k*
by using SHA512. The value *s* is used to compute the point $s\cdot B$ that
constitutes the public key.
One might say that the pair $(s,k)$ is the actual secret key.

2. **Signing**
To sign a message *m* using secret key *sk* and public key *pk*,
the following algorithm is executed.
    1. $(s,k)\leftarrow$ *SHA512(sk)*.
    2. $r\leftarrow$ *SHA512(k+m)*
    3. $R\leftarrow r\cdot B$
    4. $h\leftarrow$ *SHA512(R+pk+m)*
    5. $S=(r+h)\cdot a$
    6. return $(R,S)$

3. **Verifying**
To verify signature $(R,S)$ for message *m* against public key *pk=A*
    1. $P\leftaqrrow S\cdot B$
    2. $h\leftarrow$ *SHA512(R+pk+m)*
    3. $Q\leftarrow R+h\cdot A$
    4. return ``valid`` if and only $P=Q$



