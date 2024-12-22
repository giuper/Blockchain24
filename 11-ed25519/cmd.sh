#!/usr/bin/bash

stb='goAlgorand'
cntr='SXWZZSNJZIKBWG2QZHVVAMEFGFJIKRYXRWYN3R7S54GGJ3CGVFZB7FTEBI'

signer='Accounts/signer'
signerMnem=${signer}'.mnem'
signerAddr=${signer}'.addr'
signerSK=${signer}'.sk'
signerSKK=${signer}'.skk'
signerAccount=`cat ${signerAddr}`

creator='Accounts/creator'
creatorAddr=${creator}'.addr'
creatorAccount=`cat ${creatorAddr}`

echo -e "Creator account:         \033[31;1m${creatorAccount}\033[0m"
echo -e "Signer account:          \033[31;1m${signerAccount}\033[0m"
echo
echo -e "\033[32;1m"
~/node/algokey import -m "`cat ${signerMnem}`" --keyfile ${signerSK}
echo -e "\033[0m"

echo -e "Secret key in:           \033[31;1m${signerSK}\033[0m"
echo

strenc=`python3.10 -c "import os, base64; print(base64.b64encode(b'$stb').decode('utf-8'))"`
strdec=`python3.10 -c "import os, base64; print(base64.b64decode(b'$strenc').decode('utf-8'))"`
echo -e "the string to be signed: \033[31;1m${stb}\033[0m"
echo -e "in base64:               \033[31;1m${strenc}\033[0m"
echo -e "decoding:                \033[31;1m${strdec}\033[0m"
echo
echo -e "signing:                 \033[31;1m${strenc}\033[0m"
echo -e "with key found in        \033[31;1m${signerSK}\033[0m"
echo -e "for contract             \033[31;1m${cntr}\033[0m"
~/node/goal clerk tealsign --data-b64 ${strenc}  --contract-addr ${cntr} --keyfile ${signerSK}

echo
echo -e "signing:                 \033[31;1m${strenc}\033[0m"
echo -e "with key found in        \033[31;1m${signerSKK}\033[0m"
echo -e "for contract             \033[31;1m${cntr}\033[0m"
~/node/goal clerk tealsign --data-b64 ${strenc}  --contract-addr ${cntr} --keyfile ${signerSKK}

