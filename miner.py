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
try:
    import winsound#probably doesnt work on linux, fuck linux
except:
    pass

root = Tk()
root.configure(background='black')
root.title("MoagCoin")
try:
    root.iconbitmap('res\\icon.ico')
except:
    try:
        root.iconbitmap('res/icon.ico')#fuckin linux users, man. will this work? idk
    except:
        pass
frames = [PhotoImage(file='res\\MoagCoin.gif',format = 'gif -index %i' %(i)) for i in range(79)]


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

music = ["money","keygen","bangarang","midi","sprites","minz","tripoloski","tiananmen"]#'minz' is the audio from a lineage rom review btw

try:
    winsound.PlaySound("res\\"+music[random.randint(0,len(music)-1)]+".wav", winsound.SND_ASYNC)#in error catch thingy because fuck linux
except:
    pass#in case music is deleted or linux is used

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
    motd = ["change da world.\nmy final message.\ngoodbye","fortnite سيئة minecraft\nجيدة أكره الناس العاديين","we like fortnite","to the moon!","pee pee poo poo","i hate women and minorities","a girl is sitting next to me\nright now what do i do","I guess they never miss, huh?","run on htc bolt for more faster","john madden john madden john madden","lol daddy good shit","i mean yes i love the kids","burger king floor 2 of waterloo station","powered by droidchan","anime girl in laser machine","just found out about racism...","does belle delphine accept moagcoin","n word","Epstein made his billions with moagCoin","Epstein seal of approval","Nonce!","moagCoin remembers 9/11","ah ah ah oooh yeah","o, the pelican. so smoothly doth\nhe crest. a wind god!","moagcoin value provided by ALLAH","which chipmunk got the most crypto?","bitconnect v2","blockchain AI says: buy high sell low!","le funni messaege","F R E E  P A L E S T I N E  YOU WILL 9/11\nنحيي لرجال القسام!\nHACKED BY SYRIAN ELECTRONIC ARMY\nنحيي لرجال القس! YOU WILL 9/11"]
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

class miner():#Handles the proof of work mining of blocks - do not edit this, or mined blocks will not verify properly and you'll have wasted a bunch of CPU cycles
    def __init__(self):
        self.quit = True#Tells mining thread when to quit, is toggled by button
        self.size = 80#Cannot be changed, or your confirmed blocks will be rejected
    def miner(self):
        while self.quit == False:
            print("Starting miner...")
            found = False
            time.sleep(1)
            publicAddress = read_wallet()['public_key']
            blockRequest = {"header":"request-block","address":publicAddress}
            block = requests.get('http://35.209.72.253:443/unclaimedBlock')
            block = ast.literal_eval(block.text)
            if block != False:
                print("Got block "+str(block["hash"]))
                challenge = block["hash"] + str(self.size)
                start = time.time()
                while self.quit == False and found == False:
                    answer = "".join(random.choice(string.ascii_lowercase+
                                       string.ascii_lowercase+
                                       string.digits) for x in range(self.size))
                    attempt = challenge+answer
                    solution = hashlib.sha256(attempt.encode()).hexdigest()
                    if solution.startswith('000000'):#DONT change this either, will be rejected by server
                        found = True
                        print("BLOCK MINED! Time taken:", time.time()-start)
                        print(solution)
                        start = time.time()
                        block["attempt"] = attempt
                        block["miner"] = publicAddress
                        time.sleep(1)
                        res = requests.post("http://35.209.72.253:443/confirmBlock", data=block)
            else:
                print("Mining error, server did not return block")
Miner = miner()
def minerButton(minerClass):#run when the mining button is pressed, best not to edit this
    if minerClass.quit == True:
        minerClass.quit = False
        btnMine_text.set("STOP MINING")
        print("""\nWARNING!
MoagCoin mining is CPU intensive.
Depending on device performance, mining MoagCoin may take time.
If you stop mining, you will lose the block that's currently being mined.""")
        minerThread = threading.Thread(target=Miner.miner).start()#Starts miner thread seperate to rest of UI thread
    else:
        print("MINING STOPPING...")
        minerClass.quit = False
        btnMine_text.set("START MINING")

#this is pretty much all UI stuff, mostly safe to edit. do not touch bottom 2 lines or UI will break
label = Label(root,background="black",text="MOAGCOIN INTERFACE v1",foreground="green",font=("Courier New", 24))
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
btnMine = Button(root,background="black",textvariable=btnMine_text,foreground="green",font=("Courier New", 24), command=lambda: minerButton(Miner))
btnMine.pack()
btnMusic = Button(root,background="black",text="STOP MUSIC",foreground="green",font=("Courier New", 16), command=lambda: winsound.PlaySound(None, winsound.SND_PURGE))
btnMusic.pack()


root.after(0, update, 0)
root.mainloop()
