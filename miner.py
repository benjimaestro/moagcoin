#################################
##ONLY TO BE DISTRIBUTED ON THE##
##EPIC GAMES STORE!!!!!##########
#################################

from tkinter import *
import time
import os
import random
import requests
import ast
import threading
import string
import hashlib
import ecdsa
import base64
from ast import literal_eval
import multiprocessing as mp

def generate_wallet():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    private_key = sk.to_string().hex() #convert your private key to hex
    vk = sk.get_verifying_key() #this is your verification key (public key)
    public_key = vk.to_string().hex()
    #encode key to make it shorter
    public_key = base64.b64encode(bytes.fromhex(public_key))
    file_contents = {"public_key":public_key.decode(),"private_key":private_key}
    with open("wallet", "w") as f:
        f.write(str(file_contents))

def sign_ECDSA_msg(message,private_key):#Signs messages with your private key - DO NOT FUCK WITH THIS because if you mess it up, none of your requests will be verified
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message#Returns b64 signature to make it shorter

def send_transaction(addr_from, private_key, addr_to, amount, message):#Does what the name says, best not to mess with too much or you may lose out on your money
    if len(private_key) == 64:
        if type(amount) == int or type(amount) == float:
            signature, message = sign_ECDSA_msg(message,private_key)
            timeNow = time.time()
            toHash = addr_to + addr_from + str(timeNow)+"80"
            payload = {"from": addr_from,
                       "to": addr_to,
                       "amount": amount,
                       "signature": signature.decode(),
                       "message": message,
                       "timestamp":timeNow,
                       "nonce":random.randint(1,2147483646),
                       "header":"transaction",
                       "hash":hashlib.sha256(toHash.encode()).hexdigest(),
                       "validated": "unclaimed"}
            print(payload)
            res = requests.post("http://35.209.72.253:443/addTrans", data=payload)
            if res.text == "True":
                return True
            else:
                return False
        else:
                return False
    else:
        return False

def read_wallet():#Reads wallet file and returns dictionary
    try:
        with open("wallet") as f:
            content = f.readlines()
        return literal_eval(content[0])
    except FileNotFoundError:
        generate_wallet()
        with open("wallet") as f:
            content = f.readlines()
        return literal_eval(content[0])

def update(ind):#runs coin gif
    if ind > 78:
        ind = 1
    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    root.after(78, update, ind)
def motd():#returns le funni message
    motd = ["change da world.\nmy final message.\ngoodbye","fortnite سيئة minecraft\nجيدة أكره الناس العاديين","we like fortnite","to the moon!","pee pee poo poo","a girl is sitting next to me\nright now what do i do","I guess they never miss, huh?","run on htc bolt for more faster","john madden john madden john madden","burger king floor 2 of waterloo station","powered by droidchan","anime girl in laser machine","just found out about racism...","does belle delphine accept moagcoin","n word","Make billions with moagCoin","ah ah ah oooh yeah","o, the pelican. so smoothly doth\nhe crest. a wind god!","which chipmunk got the most crypto?","bitconnect v2","blockchain powered by DROIDCHAN AI"]
    return motd[random.randint(0,len(motd)-1)]
def txWindow():#Transaction window, called when payment window button is pressed, pretty safe to mess around with/theme
    publicAddress = read_wallet()['public_key']
    tx = Toplevel()
    tx.title("Transaction Window")
    tx.configure(background='black')
    label = Label(tx,background="black",text="Transfer MoagCoin",foreground="green",font=("Courier New", 24))
    label.pack()
    label = Label(tx,background="black",text="Recipient address",foreground="green",font=("Courier New", 16))
    label.pack()
    address = Entry(tx, bg="gray10",fg="green",relief="flat")
    address.pack(fill="x")
    label = Label(tx,background="black",text="Amount to transfer",foreground="green",font=("Courier New", 16))
    label.pack()
    amount = Entry(tx, bg="gray10",fg="green",relief="flat")
    amount.pack(fill="x")
    label = Label(tx,background="black",text="Optional message",foreground="green",font=("Courier New", 16))
    label.pack()
    msg = Entry(tx, bg="gray10",fg="green",relief="flat")
    msg.pack(fill="x")
    padding = Label(tx,background="black",text=" ",font=("Courier New", 18))
    padding.pack()
    confirm = Button(tx,background="black",text="CONFIRM PAYMENT",foreground="green",font=("Courier New", 24),command=lambda: [send_transaction(publicAddress,read_wallet()['private_key'],address.get(),float(amount.get()),msg.get()),tx.destroy()])
    confirm.pack()
    label = Label(tx,background="black",text=" ",foreground="green",font=("Courier New", 16))
    label.pack()
    label = Label(tx,background="black",text="All payments are non refundable.\nMake SURE the address entered is 100% correct.\nIf the address is incorrect, you will lose the coins.\nTransaction must be mined before it appears\nin recipient's balance (it is not immediate).",foreground="green",font=("Courier New", 12))
    label.pack()

def wallet():#Wallet window, called when open wallet is pressed, fairly safe to modify and theme
    publicAddress = read_wallet()['public_key']#DONT GIVE AWAY YOUR FUCKING PRIVATE KEY, BE CAREFUL THAT YOU'RE NOT MESSING WITH THAT
    balance = requests.post('http://35.209.72.253:443/balance', data={'address': publicAddress})
    transactions = requests.post('http://35.209.72.253:443/getTrans', data={'address': publicAddress})
    transactions = ast.literal_eval(transactions.text)
    top = Toplevel()
    top.title("Wallet")
    top.configure(background='black')
    label = Label(top,background="black",text="MoagCoin Balance",foreground="green",font=("Courier New", 24))
    label.pack()   
    lblBalance = Label(top,background="black",text=balance.text,foreground="green",font=("Courier New", 44))
    lblBalance.pack()
    padding = Label(top,background="black",text=" ",font=("Courier New", 18))
    padding.pack()
    txtAddress = Text(top, height=2, borderwidth=0,bg="black",fg="green")
    txtAddress.insert(1.0, "Address: "+publicAddress)
    txtAddress.pack()
    txtAddress.configure(state="disabled")
    txtAddress.configure(inactiveselectbackground=txtAddress.cget("selectbackground"))
    padding = Label(top,background="black",text=" ",font=("Courier New", 18))
    padding.pack()
    label = Label(top,background="black",text="Transactions",foreground="green",font=("Courier New", 24))
    label.pack()
    listbox = Listbox(top,foreground="green",bg="black",relief="flat")
    listbox.pack(fill="x")
    btnTx = Button(top,background="black",text="OPEN PAYMENT WINDOW",foreground="green",font=("Courier New", 24),command=txWindow)
    btnTx.pack()
    for block in transactions:#Loops through all your transactions and lists them
        if block["from"] == publicAddress:
            listbox.insert("end", "TO: "+str(block["to"]))
            listbox.insert("end", "   AMOUNT: "+str(block["amount"]))
            listbox.insert("end", "   MESSAGE: "+str(block["message"]))
            listbox.insert("end", "   TIME: "+str(block["timestamp"]))
            listbox.insert("end", "   HASH: "+str(block["hash"]))
            listbox.insert("end", "   BLOCK STATUS: "+str(block["validated"]))
            listbox.insert("end", "-----------------")
        else:
            listbox.insert("end", "FROM: "+str(block["from"]))
            listbox.insert("end", "   AMOUNT: "+str(block["amount"]))
            listbox.insert("end", "   MESSAGE: "+str(block["message"]))
            listbox.insert("end", "   TIME: "+str(block["timestamp"]))
            listbox.insert("end", "   HASH: "+str(block["hash"]))
            listbox.insert("end", "   BLOCK STATUS: "+str(block["validated"]))
            listbox.insert("end", "-----------------")

##        if mp.cpu_count() == 1:                         #This block determintes how many processes should be spawned
##            self.cores = 1                              #when mining is done with multiprocessing
##        if mp.cpu_count() > 1 and mp.cpu_count() <= 6:  #it's OK to modify this but keep in mind that your PC will
##            self.cores = mp.cpu_count() - 1             #slow considerably if you don't keep some cores open.
##        if mp.cpu_count() > 6:                          #
##            self.cores = mp.cpu_count() - 2             #

class varSave():
    def __init__(self):
        self.quit = True

def miner(vs,quitEvent):
    procs = []#Stores processes, best not to mess with
    publicAddress = read_wallet()['public_key']

    if mp.cpu_count() == 1:                         #This block determintes how many processes should be spawned
        cores = 1                                   #when mining is done with multiprocessing
    if mp.cpu_count() > 1 and mp.cpu_count() <= 6:  #it's OK to modify this but keep in mind that your PC will
       cores = mp.cpu_count() - 1                   #slow considerably if you don't keep some cores open.
    if mp.cpu_count() > 6:                          #
       cores = mp.cpu_count() - 2                   #
    
    print("Starting miner with "+str(cores)+" cores...")
    print("SICKO MODE ENGAGED, using "+str(cores)+" cores!")
    while quitEvent.is_set() == False:
        found = False
        event = mp.Event()
        time.sleep(1)
        blockRequest = {"header":"request-block","address":publicAddress}
        block = requests.get('http://35.209.72.253:443/unclaimedBlock')
        block = ast.literal_eval(block.text)
        print("\nGot block "+str(block["hash"]))
        print("Mining...")
        if block != False:
            for i in range(cores):#Creates new mining process depending on how many CPU cores you have
                p = mp.Process(target=proofOfWork,args=(event,block,publicAddress,))
                p.start()#Spawn new process to mine block
                procs.append(p)#Adds processes to a list so they can be accessed later
            while found == False and vs.quit == False:
                if event.is_set():
                    for process in procs:#Loops through process list to kill processes that did not complete the block in tie
                        process.terminate()
                        found = True
                    procs.clear()
                time.sleep(0.5)
            found = False
        else:
            print("Mining error, server did not return block")
    if quitEvent.is_set():#Kill processes if stop button pressed
        for process in procs:
            process.terminate()
        print("Miner stopped successfully!")

def proofOfWork(event, block, publicAddress):#Core mining module, does the work when mining
    start = time.time()
    found = False
    challenge = block["hash"] + "80"
    while found == False:
        answer = "".join(random.choice(string.ascii_lowercase+
                           string.ascii_lowercase+
                           string.digits) for x in range(80))
        attempt = challenge+answer
        solution = hashlib.sha256(attempt.encode()).hexdigest()
        if solution.startswith('000000'):#DONT change this either, will be rejected by server - should be 000000
            found = True
            print("\nBLOCK MINED! Time taken:", time.time()-start)
            print("Timestamp:",time.time())
            print(solution)
            start = time.time()
            block["attempt"] = attempt
            block["miner"] = publicAddress
            time.sleep(1)
            res = requests.post("http://35.209.72.253:443/confirmBlock", data=block)
            event.set()
    return True
    
def minerButton(vs,quitEvent):#run when the mining button is pressed, best not to edit this
    if vs.quit == True:
        vs.quit = False
        quitEvent.clear()
        btnMine_text.set("STOP MINING")
        print("""\nWARNING!
MoagCoin mining is CPU intensive.
Depending on device performance, mining MoagCoin may take time.
If you stop mining, you will lose the block that's currently being mined.""")
        #minerThread = threading.Thread(target=Miner.miner).start()#Starts miner thread seperate to rest of UI thread
        minerProc = mp.Process(target=miner,args=[vs,quitEvent,]).start()

    else:
        print("MINING STOPPING, PLEASE WAIT A FEW SECONDS FOR PROCESSES TO END!")
        vs.quit = True
        quitEvent.set()
        btnMine_text.set("START MINING")

if __name__ == '__main__':
    mp.freeze_support()#Important for compilation with PyInstaller, won't work properly without it
    print("""
 ███▄ ▄███▓ ▒█████   ▄▄▄        ▄████  ▄████▄   ▒█████   ██▓ ███▄    █ 
▓██▒▀█▀ ██▒▒██▒  ██▒▒████▄     ██▒ ▀█▒▒██▀ ▀█  ▒██▒  ██▒▓██▒ ██ ▀█   █ 
▓██    ▓██░▒██░  ██▒▒██  ▀█▄  ▒██░▄▄▄░▒▓█    ▄ ▒██░  ██▒▒██▒▓██  ▀█ ██▒
▒██    ▒██ ▒██   ██░░██▄▄▄▄██ ░▓█  ██▓▒▓▓▄ ▄██▒▒██   ██░░██░▓██▒  ▐▌██▒
▒██▒   ░██▒░ ████▓▒░ ▓█   ▓██▒░▒▓███▀▒▒ ▓███▀ ░░ ████▓▒░░██░▒██░   ▓██░
░ ▒░   ░  ░░ ▒░▒░▒░  ▒▒   ▓▒█░ ░▒   ▒ ░ ░▒ ▒  ░░ ▒░▒░▒░ ░▓  ░ ▒░   ▒ ▒ 
░  ░      ░  ░ ▒ ▒░   ▒   ▒▒ ░  ░   ░   ░  ▒     ░ ▒ ▒░  ▒ ░░ ░░   ░ ▒░
░      ░   ░ ░ ░ ▒    ░   ▒   ░ ░   ░ ░        ░ ░ ░ ▒   ▒ ░   ░   ░ ░ 
       ░       ░ ░        ░  ░      ░ ░ ░          ░ ░   ░           ░ 
                                      ░                                
                    --===============================--
                          MOAGCOIN MINER & WALLET
                    --===============================--
""")#highly important performance enhancing ascii art

    root = Tk()
    root.configure(background='black')
    root.title("MoagCoin")
    vs = varSave()
    quitEvent = mp.Event()
    try:
        root.iconbitmap('res\\icon.ico')
    except:
        try:
            root.iconbitmap('res/icon.ico')#fuckin linux users, man. will this work? idk
        except:
            pass
    frames = [PhotoImage(file='res\\MoagCoin.gif',format = 'gif -index %i' %(i)) for i in range(79)]
    #this is pretty much all UI stuff, mostly safe to edit. do not touch bottom 2 lines or UI will break
    label = Label(root,background="black",text="MOAGCOIN INTERFACE v2",foreground="green",font=("Courier New", 24))
    label.pack()
    label = Label(root,background="black")
    label.pack()
    lblMotd = Label(root,background="black",text=motd(),foreground="green",font=("Courier New", 18))
    lblMotd.pack()
    padding = Label(root,background="black",text=" ",font=("Courier New", 18))
    padding.pack()
    btnWallet = Button(root,background="black",text="OPEN WALLET",foreground="green",font=("Courier New", 24),command=wallet)
    btnWallet.pack()
    btnMine_text = StringVar()
    btnMine_text.set("START MINING")
    btnMine = Button(root,background="black",textvariable=btnMine_text,foreground="green",font=("Courier New", 24), command=lambda: minerButton(vs,quitEvent))
    btnMine.pack()
    root.after(0, update, 0)
    root.mainloop()
