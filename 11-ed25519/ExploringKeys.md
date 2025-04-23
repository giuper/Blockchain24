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
Specifically,
we start from an elliptic curve in Montgomery form

$$Bv^2=u^3+Au^2+u$$

with $A\ne\pm 2$ and $B\ne 0$ and we obtain the twisted Edwards form 

$$ax^2+y^2=1+dx^2y^2$$

with $a,d\ne 0$ and $a\ne d$ by applying the map

$$(u,v)\rightarrow (x,y)=\left(\frac{u}{v},\frac{u-1}{u+1}\right)$$

which sets $a=(A+2)/B$ and $d=(A-2)/B$.

In Ed25519, we use
[Curve25519](https://www.rfc-editor.org/rfc/rfc7748#section-4.1),
with $B=1$ and $A=48662$ over the field modulo the prime $q=2^{255}-19$.
Curve25519 has the following twisted Edwards form 

$$-x^2+y^2=1-\frac{121665}{121666} x^2y^2.$$

A point $(x,y)$ over the Edwards curve is represented in extended coordinates
$(X,Y,Z,T)$ such that


$$x=\frac{X}{Z},\qquad y=\frac{Y}{Z}, \qquad x\cdot y=\frac{T}{Z}.$$

Note that the extended coordinates are not unique. Thus to check if
$(X_0,Y_0,Z_0,T_0)$ and $(X_1,Y_1,Z_1,T_1)$ represent the same point 
$(x,y)$ one must check that
$$X_0\cdot Z_1=X_1\cdot Z_0,\qquad Y_0\cdot Z_1=Y_1\cdot Z_0$$

### Secret and Public key
The secret key *sk* is a 256-bit random value and the public key *pk* is a multiple
of the base point *B*.
For Ed25519, the point *B* of order $q/8=2^{252}+27742317777372353535851937790883648493$ is inherited from the specification of Curve25519 and it 
has the following two coordinates:

$$x=15112221349535400772501151409588531511454012693041857206046113283949847762202$$
and 
$$y=46316835694926478169428394003475163141307993866256225615783033603165251855960.$$

### Extracting secret/public key from the mnemonic
We assume to have a mnemonic stored in file ```account.mnem```.

#### Step 1: from mnem
The python program [ed25519keys.py](./ed25519keys.py) reads the mnemonic from a mnem file and 
performs the following:
1. obtains *SK64enc* from ```mnemonic.to_private_key```
2. decodes *sK64enc* from base64 encoding to obtain *SK64* and sets *sk=SK64[:32]* and *pk=SK64[32:]*
3. *sk* is the private key and *pk* is the *encoded* point of the public key (see Step 4)
4. computed *SHA512(sk)* and splits the 64 bytes obtained in 2 32 byte quantity *s* and *k*
5. the integer *s* is from the first 256 bits of *SHA512(sk)* and the point *PS=sB* that consitutes the public key is obtained by multiplying the base point *B* by *s*
6. the four extended coordinates of *B* and *PS* are printed

#### Step 2: from addr
The python program ```ed25519keys.py``` reads an algorand address from an addr file
and performs the following:
1. Append "======" to the addr to obtain a valid base32 encoding
2. Decode the encoding thus to obtain a compress point as specified
in the 
[RFC](https://www.rfc-editor.org/rfc/rfc8032#section-5.1.2)
3. Decompress the point and print the extended coordinates of the point

#### Step 3: using the package ed25519.py
In this step the program uses the secret key to obtain the public key through a method from
the package ed25519.py (an open source python implementation of the signature scheme).

#### Step 4: using the second half of SK64
In this step the program uses the secondo half of SK64 as computed in Step 1. 


#### Step 5: computing the Algorand address
In the final step we close the circle: we compute the Algorand address from the point *PS* obtained
in Step 1. Specifically,
1. *PS* is compressed (as specified in the 
[RFC](https://www.rfc-editor.org/rfc/rfc8032#section-5.1.2))
2. the compress point is passed through SHA512/256 and the last 4 bytes are appended to the compressed point to obtain the marshalled point
3. the marshalled point is base32 encoded and the last six "=" are removed to obtain
the Algorand address



### Documents

[EdDSA RFC](https://www.rfc-editor.org/rfc/rfc8032)
