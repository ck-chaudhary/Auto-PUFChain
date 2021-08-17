# Code for Peer Node interfacing

import json
from web3 import Web3
import time
import os
import sys

node_url = 'HTTP://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(node_url))


print("connected = ",w3.isConnected())

w3.eth.defaultAccount = w3.eth.accounts[9]
print(w3.eth.blockNumber)

contract_address_file = open("contract_address.txt","r")
cont = contract_address_file.read()
print(cont)


contract_address = w3.toChecksumAddress(cont)
abi = json.loads('[{"constant":true,"inputs":[{"name":"_identifier","type":"uint256"}],"name":"checkOwnership","outputs":[{"name":"_ownerName","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"node","type":"address"}],"name":"KeyEnroll","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"peer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_identifier","type":"uint256"}],"name":"authenticateDevice","outputs":[{"name":"_challenge","type":"int256[]"},{"name":"_response","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_identifier","type":"uint256"},{"name":"buyer","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_identifier","type":"uint256"},{"name":"_owner","type":"address"},{"name":"_challenge","type":"int256"},{"name":"_response","type":"uint256"}],"name":"registerDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"TA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"consortium","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"node","type":"address"}],"name":"addNode","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"idInfo","outputs":[{"name":"owner","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');
deployed_contract = w3.eth.contract(address= contract_address, abi= abi)
print(deployed_contract.address)



choice=True
while choice:
    print ("""
    1.Check Ownership
    2.Authenticate device
    3.Transfer Ownership  
    3.Exit/Quit
    """)
    choice=input("What would you like to do? ") 
    if choice=="1":
        device_id = int(input("Enter the unique id for the device: "))
        owner = deployed_contract.functions.checkOwnership(device_id).call()
        print("Owner of device id:",device_id,"is ",owner)
       
    elif choice=="2":
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
            #auth[device_id] = 1
            print("Device authenticated !!! ,proceed for ownership transfer")
        else:
            print("Device authentication failed !")
 
    elif choice=="3":
        device_id = int(input("Enter the device id you would like to check ownership of: "))
        buyer = input("Whom do you want to transfer the ownership to: ")
        # Transferring the ownership to authenticated peer
        print("Previous Owner:", deployed_contract.functions.checkOwnership(device_id).call())
        tx_hash = deployed_contract.functions.transferOwnership(device_id, buyer).transact()
        #print(tx_hash)
        print("Current Owner:", deployed_contract.functions.checkOwnership(device_id).call())
        print("\n Ownership Transferred Successfully !!!")

    elif choice=="4":
      print("\n Goodbye")
      break        
    elif choice !="":
      print("\n Not Valid Choice Try again")