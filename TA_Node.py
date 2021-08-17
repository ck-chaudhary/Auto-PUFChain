# Code for TA node interfacing
# connect Peer_node for the peer interface
import json
from web3 import Web3
import time
import os
import sys
import time
import ipfsApi

node_url = 'HTTP://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(node_url))


api = ipfsApi.Client('127.0.0.1', 5001)

print("connected = ",w3.isConnected())

w3.eth.defaultAccount = w3.eth.accounts[1]
print(w3.eth.blockNumber)


byte_code = '608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610d7d806100606000396000f3006080604052600436106100a3576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168062402218146100a8578063103b14b414610115578063116a01a41461015857806325d1034e146101c557806329507f731461028f5780634618a426146102dc5780635c5ebebf1461033d5780639ad18765146103aa5780639d95f1cc14610401578063f09f6cb014610444575b600080fd5b3480156100b457600080fd5b506100d3600480360381019080803590602001909291905050506104b1565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561012157600080fd5b50610156600480360381019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506104f1565b005b34801561016457600080fd5b50610183600480360381019080803590602001909291905050506106b8565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156101d157600080fd5b506101f0600480360381019080803590602001909291905050506106f6565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561023757808201518184015260208101905061021c565b50505050905001838103825284818151815260200191508051906020019060200280838360005b8381101561027957808201518184015260208101905061025e565b5050505090500194505050505060405180910390f35b34801561029b57600080fd5b506102da60048036038101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506107cc565b005b3480156102e857600080fd5b5061033b60048036038101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019092919080359060200190929190505050610924565b005b34801561034957600080fd5b5061036860048036038101908080359060200190929190505050610b5d565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156103b657600080fd5b506103bf610b9b565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561040d57600080fd5b50610442600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610bc0565b005b34801561045057600080fd5b5061046f60048036038101908080359060200190929190505050610d13565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006003600083815260200190815260200160002060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b60008060009050600091505b600180549050821015610589573373ffffffffffffffffffffffffffffffffffffffff1660018381548110151561053057fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16141561057c57600190505b81806001019250506104fd565b60018114151561064d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252604d8152602001807f54686973206e6f64652063616e277420456e726f6c6c20612070656572206e6f81526020017f64652c204f6e6c7920544120697320656c696769626c6520746f20656e726f6c81526020017f6c20612070656572206e6f64650000000000000000000000000000000000000081525060600191505060405180910390fd5b60028390806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050505050565b6002818154811015156106c757fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6060806003600084815260200190815260200160002060010180548060200260200160405190810160405280929190818152602001828054801561075957602002820191906000526020600020905b815481526020019060010190808311610745575b50505050509150600360008481526020019081526020016000206002018054806020026020016040519081016040528092919081815260200182805480156107c057602002820191906000526020600020905b8154815260200190600101908083116107ac575b50505050509050915091565b6003600083815260200190815260200160002060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156108cb576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602d8152602001807f4f6e6c7920646576696365206f776e65722063616e207472616e73666572207481526020017f6865206f776e6572736869702e0000000000000000000000000000000000000081525060400191505060405180910390fd5b806003600084815260200190815260200160002060000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050565b60008060009050600091505b6001805490508210156109bc573373ffffffffffffffffffffffffffffffffffffffff1660018381548110151561096357fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156109af57600190505b8180600101925050610930565b600181141515610a80576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252604a8152602001807f54686973206e6f64652063616e2774207265676973746572207468652064657681526020017f6963652c204f6e6c7920544120697320656c696769626c6520746f207267697381526020017f746572206465766963650000000000000000000000000000000000000000000081525060600191505060405180910390fd5b846003600088815260200190815260200160002060000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506003600087815260200190815260200160002060010184908060018154018082558091505090600182039060005260206000200160009091929091909150555060036000878152602001908152602001600020600201839080600181540180825580915050906001820390600052602060002001600090919290919091505550505050505050565b600181815481101515610b6c57fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610caa576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602a8152602001807f4f6e6c7920636f6e7472616374206465706c6f7965722063616e20616464207481526020017f68657365206e6f6465730000000000000000000000000000000000000000000081525060400191505060405180910390fd5b60018190806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050565b60036020528060005260406000206000915090508060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050815600a165627a7a723058207416e977303d9c02b495f39549f90f288817397b76718224a30b178847ec6d060029';
abi = json.loads('[{"constant":true,"inputs":[{"name":"_identifier","type":"uint256"}],"name":"checkOwnership","outputs":[{"name":"_ownerName","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"node","type":"address"}],"name":"KeyEnroll","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"peer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_identifier","type":"uint256"}],"name":"authenticateDevice","outputs":[{"name":"_challenge","type":"int256[]"},{"name":"_response","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_identifier","type":"uint256"},{"name":"buyer","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_identifier","type":"uint256"},{"name":"_owner","type":"address"},{"name":"_challenge","type":"int256"},{"name":"_response","type":"uint256"}],"name":"registerDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"TA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"consortium","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"node","type":"address"}],"name":"addNode","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"idInfo","outputs":[{"name":"owner","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');

obj = w3.eth.contract(abi=abi, bytecode=byte_code)
tx_hash = obj.constructor().transact()
#print(w3.toHex(tx_hash))

#contract = w3.eth.contract(address= contract_address, abi= abi)

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

deployed_contract = w3.eth.contract(
	address=tx_receipt.contractAddress,
	abi=abi
	)

print(deployed_contract.address)

try:
    contract_address_file = open("contract_address.txt","w")
    # Do something with the file
except IOError:
    print("File not accessible")
finally:
	contract_address_file.write(str(deployed_contract.address))

	contract_address_file.close()



#Adding some default TA nodes
TANodes = []
for i in range(3):
    TANodes.append(w3.eth.accounts[i])
    
print(TANodes)

for i in TANodes:
    tx_hash = deployed_contract.functions.addNode(i).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    print(w3.toHex(tx_hash))

# Default peer node registration
peerNodes = []
for i in range(3):
    peerNodes.append(w3.eth.accounts[5+i])
    
print(peerNodes)

for i in peerNodes:
    tx_hash = deployed_contract.functions.KeyEnroll(i).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    print(w3.toHex(tx_hash))

auth ={}


choice=True
while choice:
    print ("""
    1.Add a TA node
    2.Add a Peer node
    3.Register a device
    4.Check Ownership
    5.Authenticate device
    6.Transfer Ownership
    7.Exit/Quit
    """)
    choice=input("What would you like to do? ")
    if choice=="1":
        x = input("Enter the address of the node: ") 
        tx_hash = deployed_contract.functions.addNode(x).transact() 
        w3.eth.waitForTransactionReceipt(tx_hash)
        print("\n TA node Added with transaction hash :",w3.toHex(tx_hash)) 

    elif choice=="2":
        x = input("Enter the address of a peer node :")
        tx_hash = deployed_contract.functions.addNode(x).transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        print("\n Peer node Added with transaction hash :",w3.toHex(tx_hash)) 	
      
    elif choice=="3":
        device_id = int(input("Enter the unique id for the device: "))
        board = input("Enter the board number: ")
        file_name = input("Enter the name of challenge file: ")
        chal_no = int(input("How many CRP would you like to keep: "))
        command = 'sudo python APUF_64_1.py ' + str(board) + ' ' + file_name
        os.system(command)
        
        x =[]
        y =[]
        ipfs_chal_file = api.add(file_name)
        print(ipfs_chal_file)
        response_file = 'a_puf_golden_' + str(board) + '.txt'
        ipfs_resp_file = api.add(response_file)
        print(ipfs_resp_file)
        with open(file_name) as f1, open(response_file) as f2:
            x = f1.read().split('\n')
            y = f2.read().split('\n')
        for i in range(chal_no):
            print(x[i],y[i])
        
        chal = x
        res = y
        for i in range(chal_no):
            tx_hash = deployed_contract.functions.registerDevice(device_id, w3.eth.accounts[1],  int(chal[i]), int(res[i])).transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
            print(w3.toHex(tx_hash))

        print("Device got registered succesfully !!!")
 
    elif choice=="4":
        device_id = int(input("Enter the unique id for the device: "))
        owner = deployed_contract.functions.checkOwnership(device_id).call()
        print("Owner of device id:",device_id,"is ",owner)
        
    elif choice=="5":
        device_id = int(input("Enter the device id you would like to authenticate: "))
        y = deployed_contract.functions.authenticateDevice(device_id).call()
        print(len(y[0]))
        for i in range(len(y[0])):
            print(y[0][i], y[1][i])
        board = input("Enter the board number to which the device is connected: ")
        
        file2_name = 'chal_from_device_' + str(board) + '.txt'
        file_chal = open(file2_name,"a")
        for i in range(len(y[0])):
            file_chal.write(str(y[0][i]).zfill(64) + '\n')
            
        command2 = 'sudo python APUF_64_1.py ' + str(board) + ' ' + file2_name
        file_chal.close()

        os.system(command2)

        
        # response of chal_10_device
        resp = 'a_puf_golden_' + str(board) + '.txt'
        res =[]
        with open(resp) as f1:
            res = f1.read().split('\n')
        
        # Authenticating the chal-resp pairs


        flag=0
        print(y)
        test = [int(res[i]) for i in range(len(res)-1)]
        print(test)
        for i in range(len(res)-1):
            if(test[i] == y[1][i]):
                continue
            else:
                flag =1
                break;
        
        #print(flag)
        #os.system("sudo rm chal_for_device.txt")
        
        if (flag == 0) and (len(res)!= 0):
            auth[device_id] = 1
            print("Device authenticated !!! ,proceed for ownership transfer")
        else:
            print("Device authentication failed !")


    elif choice=="6":
        device_id = int(input("Enter the device id you would like to check ownership of: "))
        buyer = input("Whom do you want to transfer the ownership to: ")
        # Transferring the ownership to authenticated peer
        print("Previous Owner:", deployed_contract.functions.checkOwnership(device_id).call())
        tx_hash = deployed_contract.functions.transferOwnership(device_id, buyer).transact()
        #print(tx_hash)
        print("Current Owner:", deployed_contract.functions.checkOwnership(device_id).call())
        print("\n Ownership Transferred Successfully !!!")
        
    elif choice=="7":
      print("\n Goodbye")
      break 
    elif choice !="":
      print("\n Not Valid Choice Try again")