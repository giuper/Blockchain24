import sys
from algosdk import account, mnemonic

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()

accountName=sys.argv[1]

privateKey, address = account.generate_account()
with open(accountName+".addr",'w') as f:
    f.write(address)
with open(accountName+".mnem",'w') as f:
    f.write(mnemonic.from_private_key(privateKey))

print(f'{"Account address:":20s}{address}')
print(f'{"Account passphrase:":20s}{mnemonic.from_private_key(privateKey)}')
print("Please go to: https://bank.testnet.algorand.network/ to fund account.")



