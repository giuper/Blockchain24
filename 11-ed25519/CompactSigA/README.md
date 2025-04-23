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

## Reviewing Ed25519 Signatures

1. **Key Generation**
The secret (signing) key *sk* for Ed25519 is a 256-bit random value 
and the public (verification key *pk* is a multiple of the base point *B*.
The 256 bits of *sk* are expanded into two 256-bit valyes *s* and *k*
by using SHA512. The value *s* is used to compute the point $A=s\cdot B$ that
constitutes the public key.
One might say that the pair $(s,k)$ is the actual secret key.

2. **Signing**
To sign a message *m* using secret key *sk* and public key *pk*,
the following algorithm is executed.
    1. $(s,k)\leftarrow$ *SHA512(sk)*.
    2. $r\leftarrow$ *SHA512(k+m)*
    3. $R\leftarrow r\cdot B$
    4. $h\leftarrow$ *SHA512(R+pk+m)*
    5. $S=r+h\cdot s$
    6. return $(R,S)$

3. **Verifying**
To verify signature $(R,S)$ for message *m* against the public key *pk*
consisting of point $A$
    1. $P\leftarrow S\cdot B$
    2. $h\leftarrow$ *SHA512(R+pk+m)*
    3. $Q\leftarrow R+h\cdot A$
    4. return ``valid`` if and only $P=Q$

Note that even if the signature algorithm prescribes
the randomness of the signature $r$ to be derived
from the secret key through $k$, this is not checked at verification
time. 

## Making two signatures into one

We consider the simple case of two secret keys $sk_1$ and $sk_2$
determing integers $s_1$ and $s_2$, respectively, which in turn
determine two points $A_1=s_1\cdot B$ and $A_2=s_2\cdot B$ that
appear in the *source* public keys.

We would like the two parties owning $sk_1$ and $sk_2$
to be able to compute a signature of a message $m$ that
can be verified with respect to a *destination* public key *pk*.
For this to be non-trivial, it must be the case that only the two
parties that have access to the secret keys can compute the signature.


### Combining the public keys
We first specify how to derive a public key $A$ from $A_1$ and $A_2$.
This is simply obtained by setting $A\leftarrow A_1+A_2$.
Note that $A=s\cdot B$, for $s=s_1+s_2$.

### Combining the signatures
One might think that, since the destination public key is the sum of the 
two source public keys, it would be enough for each of the two parties
to compute its signature of the message and then the sum of two
signatures would qualify as a valid signature with respect to
the destination public key. It is easy to see that this will not work.
Instead we proceed as follows.

1. Party $i=1,2$ randomly selects $r_i\leftarrow Z_l$, sets
$R_i=r_i\cdot B$, and sends $R_i$ to the other party.
2. Party $i=1,2$ computes $R=R_1+R_2$ and sets $h\leftarrow$SHA512(R+pk+m)$.
3. Party $i=1,2$ computes *half signature* $S_i=r_i+h\cdot s_i$ and sends it
        to the other party.
4. Each party computes $S=S_1+S_2$ and outputs signature $(R,S)$

### Signature verification
Observe that 
$$S=S_1+S_2=(r_1+r_2)+h\cdot (s_1+s_2)=(r_1+r_2)+h\cdot s$$
and that
$$R=(r_1+r_2)\cdot B$
therefore we will have that
$$P=S\cdot B=((r_1+r_2)+h\cdot s)\cdot B=(r_1+r_2)\cdot B+h\cdot s\cdot B 
=R+h\cdot A=Q$$

Therefore, the same verification algorithm can be used to verify
the signature. This implies that we can use the same TEAL contract
(with the destination public key) to verify that a message has
been signed by multiple parties (i.e., the parties whose public keys
are *accumulated* into the destination public key).


### More than two parties
The generalization to more than 2 parties is straightforward.

### The implementation
We have implemented the above in the following scripts:

1. [Destination public key](00-makePKa.py).
    The destination address is obtained by specifying the files with 
    two Algorand addresses.
2. [Computing $R_i$](02-writeRa.py) The value $R_i$ is computed and written in a file. It takes as input the name of the account and the file containing the message and writes in the value in a ``.R`` file. 
This script must be executed by each player and it accesses the mnem file 
of the account specified.
3. [Computing half signature](03-signa.py) it takes as input the names of
the two accounts and accesses the respective ``.R`` files,
and the ``mnem`` file of the first account. 
It writes the *half signature* of the first account in the ``.sig`` file.
This script must be executed by each player by specifying its ownaccount as first account.
4. [Summing the half signatures](04-suma.py) it takes the names of the two account and access the respective ``.R`` and ``.sig`` files 
and outputs the signature. It must be executed only once by either one of the players (as no ``mnem`` file is accessed) 

### Computing the message
Algorand implements strict domain separation for the signature and therefore
the message to be signed depends on the specific role. In this folder we
have two script:
1. [To sign a message for TEAL code](01-makeMSGTeal.py)
This is used to compose the message to be signed for verification by a TEAL script. 
It takes as input the name of the file containing the compiled TEAL program 
(or alternatively the encoded hash of the TEAL program),
and the actual data to be signed as well 
as the name of the file that will contain the message. 
2. [To sign a payment ](01-makeMSGTx.py)
This can be used to sign a transaction. 
It takes as input the name of the file containing the unsigned transaction
and the name of the file that will contain the message. 

    1.  The script [makeTX.py](makeTX.py) can be used to construct 
        a simple payment transaction. 
        It takes as input the name of the sender account 
        and of the receiver accounts as well as the file that will contain the signed transaction.
    2.  The script [sendTX.py](sendTX.py) can be used to submit the 
        transaction created at the previous step.

