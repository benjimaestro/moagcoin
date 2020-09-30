import time
import hashlib
import threading
from flask import Flask, request
import sys
import pickle
import random
import ecdsa
import base64
node = Flask(__name__)

@node.route('/debugBC', methods=['GET', 'POST'])
def debugBC():
    try:
        return str(BC.getBlockchain())
    except Exception as e:
        print(e)

@node.route('/getTrans', methods=['GET', 'POST'])
def getTransactions():
    address = request.form['address']
    getTx = []
    for block in BC.blockchain:
        if BC.blockchain[block]["from"] == address or BC.blockchain[block]["to"] == address:
            getTx.append(BC.blockchain[block])
    return str(getTx[::-1])


def getBalance(address):
    balance = 0
    for block in BC.getBlockchain():
        if BC.blockchain[block]["from"] == address:
            balance = balance - float(BC.blockchain[block]["amount"])
        if BC.blockchain[block]["to"] == address:
            if BC.blockchain[block]["validated"] == 'validated':
                balance = balance + float(BC.blockchain[block]["amount"])
    return str(balance)

@node.route('/balance', methods=['GET', 'POST'])
def getBalanceRequest():
    address = request.form['address']
    balance = 0
    for block in BC.getBlockchain():
        if BC.blockchain[block]["from"] == address:
            balance = balance - float(BC.blockchain[block]["amount"])
        if BC.blockchain[block]["to"] == address:
            if BC.blockchain[block]["validated"] == 'validated':
                balance = balance + float(BC.blockchain[block]["amount"])
    return str(balance)

def canSpend(transaction,address):
    balance = float(getBalance(address))
    if float(balance) > float(transaction) and float(transaction) > 0.001:
        return "True"
    else:
        return "False"

@node.route('/unclaimedBlock', methods=['GET'])
def getUnclaimedBlock():
    unclaimed = []
    for block in BC.getBlockchain():
        if BC.blockchain[block]["validated"] == "unvalidated" or BC.blockchain[block]["validated"] == "unclaimed":
            unclaimed.append(BC.blockchain[block])
    return str(unclaimed[random.randint(0,len(unclaimed)-1)])

@node.route('/confirmBlock', methods=['GET', 'POST'])
def confirmBlock():
    tx = request.form
    x = 0
    if hashlib.sha256(tx["attempt"].encode()).hexdigest().startswith("0000") == True:
        if validate_signature(tx["from"],tx["signature"],tx["message"]) == True:
            timeNow = time.time()
            toHash = "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg=="+tx["miner"]+str(timeNow)+BC.getAttemptLength()

            if tx["miner"] in BC.timer and (BC.timer[tx["miner"]]-time.time()) < 3600:
                reward = (time.time()-BC.timer[tx["miner"]])/1200.0
            else:
                reward = 1
            print(reward)
            BC.timer[tx["miner"]] = time.time()
            reward = str(str(reward).split(".")[0][0])+"."+(str(reward).split(".")[1][:3])
            
            reward = {"from": "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg==",
                        "to": tx["miner"],
                        "amount": str(reward),
                        "signature": "WXMY+nUrwUzZZuBxKp2I8mJ3HsuJUXMWM+uIxalJTufCaavV0IZmELUb1ny7xnYROep6TMpluNDQ6alNf+OC0Q==",
                        "message": "MINING REWARD",
                        "timestamp":timeNow,
                        "nonce":random.randint(1,2147483646),
                        "header":"transaction",
                        "validated": "unvalidated"}
            reward["hash"] = hashlib.sha256(toHash.encode()).hexdigest()
            BC.blockchain[tx["hash"]]["validated"] = "validated"
            BC.append(reward)
            BC.saveBlockchain()
            return "True"
        else:
            return "False"
    else:
        return "False"

@node.route('/addTrans', methods=['GET', 'POST'])
def addTransaction():
    iTx = request.form
    tx = {}
    for key in iTx:
        tx[key] = iTx[key]
    toHash = tx["to"]+tx["from"]+str(tx["timestamp"])+BC.getAttemptLength()
    if canSpend(tx["amount"],tx["from"]) == "True" and tx["from"] != tx["to"]:
        if validate_signature(tx["from"],tx["signature"].encode(),tx["message"]) == True and hashlib.sha256(toHash.encode()).hexdigest() == tx["hash"]:
            tx["to"] = tx["to"].replace(" ","")
            tx["message"] = (tx["message"][:250] + '..') if len(tx["message"]) > 250 else tx["message"]
            BC.append(tx)
            BC.saveBlockchain()
            return "True"
        else:
            #print(validate_signature(tx["from"],tx["signature"].encode(),tx["message"]), hashlib.sha256(toHash.encode()).hexdigest(), tx["hash"])
            return "False"
    else:
        return 'False'

def validate_signature(public_key, signature, message):
    #print(public_key)
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    try:
        return vk.verify(signature, message.encode())
    except Exception as e:
        print(e)
        return False

class clsBlockchain():
    def __init__(self):
        self.genesis = False
        self.timer = {}
        self.blockchain = {}
    def getBlockchain(self):
        with open("blockchain.lst","rb") as f:
            try:
                self.blockchain = pickle.load(f)
            except:
                self.blockchain = {}
                timeNow  = time.time()
                toHash = "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg=="+"vCUVXCVSKnA0KEUAUtBq2qJQlVs4kcjIB2fPShbpXGoSU5W6LY+uCEc+B6jOYhhvb4Zyp7xjRLLOp202Rj/08Q=="+str(timeNow)+self.getAttemptLength()
                self.blockchain[hashlib.sha256(toHash.encode()).hexdigest()] = {"from": "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg==",
                       "to": "vCUVXCVSKnA0KEUAUtBq2qJQlVs4kcjIB2fPShbpXGoSU5W6LY+uCEc+B6jOYhhvb4Zyp7xjRLLOp202Rj/08Q==",
                       "amount": "0",
                       "signature": "ONtB++nUrfc5A+TSIQCxqLtxeSfLkBEiFHqUZu5ish6UXcSnkqDrr5H+zbg2fiuPd2/fLXYL0t08JZe61332jw==",
                       "message": "GENESIS BLOCK",
                       "timestamp":timeNow,
                       "nonce":random.randint(1,2147483646),
                       "header":"transaction",
                       "hash":hashlib.sha256(toHash.encode()).hexdigest(),
                       "validated": "unvalidated"}
                time.sleep(0.1)
                timeNow  = time.time()
                toHash = "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg=="+"vCUVXCVSKnA0KEUAUtBq2qJQlVs4kcjIB2fPShbpXGoSU5W6LY+uCEc+B6jOYhhvb4Zyp7xjRLLOp202Rj/08Q=="+str(timeNow)+self.getAttemptLength()
                self.blockchain[hashlib.sha256(toHash.encode()).hexdigest()] = {"from": "Ec53Zy1qs+VbyPZDR4D3l8I13Utns/5KoUuN6yintVI3RbJrCav3kbvBLii6QMzRW5h/2Hv53F7bI3lciT+EZg==",
                       "to": "vCUVXCVSKnA0KEUAUtBq2qJQlVs4kcjIB2fPShbpXGoSU5W6LY+uCEc+B6jOYhhvb4Zyp7xjRLLOp202Rj/08Q==",
                       "amount": "175",
                       "signature": "jkaUHhwTxQUv0VkwLjH5qeP+eKJrGH8NZQcDk0CrJKNs+LMTM/3sSRHg5Qi14ns6YnZujI9eSsAuoBcQwg76Vw==",
                       "message": "Initial",
                       "timestamp":time.time(),
                       "nonce":random.randint(1,2147483646),
                       "header":"transaction",
                       "hash":hashlib.sha256(toHash.encode()).hexdigest(),
                       "validated": "validated"}
                self.saveBlockchain()
        return self.blockchain
    def append(self,block):
        self.blockchain[block["hash"]] = block
        self.saveBlockchain()
    def getBlock(self,hash):
        return self.blockchain[hash]
    def saveBlockchain(self):
        with open('blockchain.lst', 'wb') as f:
            pickle.dump(self.blockchain, f)
    def removeFromBlockchain(self,block):
        del self.blockchain[block["hash"]]
        self.saveBlockchain()
    def getAttemptLength(self):
        return "80"

global BC
BC = clsBlockchain()
node.run(threaded=True,host='0.0.0.0',port=5555)
