#!/bin/bash

#specify your version of python
python=python3.10

account1=P1
account2=P2
account3=P3
accountMulti=M

txDir="./TX"
unsignedTX=${txDir}/"MultiPay.utx"
unsignedWithPKTX=${txDir}/"MultiPayWithPK.utx"
signedTX=${txDir}/"MultiPay.stx"

echo "Creating a 2 out of 3 multisig account"
${python} createMultiAddr.py ${account1}.addr ${account2}.addr ${account3}.addr ${accountMulti}.addr
read

mkdir -p ${txDir}
echo "Creating a multisig TX"
${python} multiPayTXComplete.py ${account1}.addr ${account2}.addr ${account3}.addr ${account1}.mnem ${account3}.mnem ${account2}.addr


