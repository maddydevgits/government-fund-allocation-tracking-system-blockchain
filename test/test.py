from web3 import Web3,HTTPProvider
import json

blockchain_server='http://127.0.0.1:7545'
web=Web3(HTTPProvider(blockchain_server))
web.eth.defaultAccount=web.eth.accounts[0]
artifact_path='../build/contracts/register.json'
contract_address='0x361ef311Fb9bD723aE7424Af6B4e86Eb2a451625'
with open(artifact_path) as f:
    contract_json=json.load(f)
    contract_abi=contract_json['abi']
contract=web.eth.contract(address=contract_address,abi=contract_abi)

#tx_hash=contract.functions.registeruser('0x92f837D7B4659659b0faf4c5a4fA49f85B1A19b8','sandhyasridamarla@gmail.com','Sandhya Sri','9014988081','finance',0,1234).transact()
#web.eth.waitForTransactionReceipt(tx_hash)
#print('Data Inserted')
#usernames,emails,names,mobiles,depts,roles,passwords=contract.functions.viewusers().call()
#print(usernames,emails,names,mobiles,depts,roles,passwords)
a=contract.functions.loginuser('0x92f837D7B4659659b0faf4c5a4fA49f85B1A19b8',123).call()
print(a)