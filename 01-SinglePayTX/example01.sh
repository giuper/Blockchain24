#!/bin/bash

ACCOUNTDir="./Accounts"
SENDER=${ACCOUNTDir}"/sender"
RECEIVER=${ACCOUNTDir}"/receiver"

TXDir="./TX"
UNSIGNEDTX=${TXDir}"/Pay.utx"
SIGNEDTX=${TXDir}"/Pay.stx"

#set goal according to installation
GOAL=../../../../goal

mkdir -p ${ACCOUNTDir}
mkdir -p ${TXDir}

echo "Creating the sender account"
python3.10 createSingle.py ${SENDER}
read
clear -x

echo "Creating the receiver account"
python3.10 createSingle.py ${RECEIVER} read
clear -x

echo "Executing a single sender payment transaction"
python3.10 payTX.py ${SENDER}.mnem ${RECEIVER}.addr 
read
clear -x

