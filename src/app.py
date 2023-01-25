from flask import Flask,render_template,request,redirect,session
from web3 import Web3,HTTPProvider
import json

def connect_blockchain_register(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/register.json'
    contract_address='0xF55A5271e73D7101a693afdE77Fb9CCFd6A22D3A'
    with open(artifact_path) as F:
        contract_json=json.load(F)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

def connect_blockchain_fund(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/funds.json'
    contract_address='0x8757E0fa2e8501d352FDE74F58A5A49E3C83EDAf'
    with open(artifact_path) as F:
        contract_json=json.load(F)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

app=Flask(__name__)
app.secret_key='Sandhya'

@app.route('/')
def homepage():
    return render_template('Home.html')

@app.route('/registration')
def registerpage():
    return render_template('Registration.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/head')
def headpage():
    return render_template('Head.html')

@app.route('/desc')
def descpage():
    return render_template('desc.html')

@app.route('/publictracking')
def publictrackingpage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_fund(0)
    _senders,_receivers,_amounts=contract.functions.viewfunds().call()
    print(_usernames,_emails,_names,_mobiles,_depts,_roles,_passwords)
    print(_senders,_receivers,_amounts)
    data=[]
    for i in range(len(_senders)):
            dummy=[]
            #sno,sender,sender dept, receiver,amount
            sindex=_usernames.index(_senders[i])
            dummy.append(_senders[i])
            dummy.append(_names[sindex])
            dummy.append(_depts[sindex])
            dummy.append(_receivers[i])
            dummy.append(_amounts[i])
            data.append(dummy)
    return render_template('publictracking.html',res=data,l=len(data))

@app.route('/newhead')
def newheadpage():
    return render_template('newhead.html')

@app.route('/newhome')
def newhomepage():
    return render_template('newhome.html')

@app.route('/newdesc')
def newdescpage():
    return render_template('newdesc.html')

@app.route('/allocatefund')
def allocatefundpage():
    return render_template('allocatefund.html')

@app.route('/logout')
def logoutpage():
    session.pop('username',None)
    return redirect('/')

@app.route('/tracking')
def trackingpage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_fund(0)
    _senders,_receivers,_amounts=contract.functions.viewfunds().call()
    print(_usernames,_emails,_names,_mobiles,_depts,_roles,_passwords)
    print(_senders,_receivers,_amounts)
    print(session['username'])
    data=[]
    for i in range(len(_senders)):
        if _senders[i]==session['username']:
            dummy=[]
            #sno,sender,sender dept, receiver,amount
            sindex=_usernames.index(_senders[i])
            dummy.append(_senders[i])
            dummy.append(_names[sindex])
            dummy.append(_depts[sindex])
            dummy.append(_receivers[i])
            dummy.append(_amounts[i])
            data.append(dummy)
    return render_template('tracking.html',res=data,l=len(data))

@app.route('/registeruser',methods=['post'])
def registeruser():
    username=request.form['username']
    email=request.form['email']
    name=request.form['name']
    mobile=request.form['mobile']
    dept=request.form['dept']
    role=request.form['role']
    password=request.form['password']
    print(username,email,name,mobile,dept,role,password)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registeruser(username,email,name,mobile,dept,int(role),int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/login')

@app.route('/loginuser',methods=['post'])
def loginuser():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginuser(username,int(password)).call()
    if state==True:
        session['username']=username
        return redirect('/newdesc')
    else:
        return(render_template('login.html',err='login failed'))

@app.route('/allocatefundform',methods=['post'])
def allocatefundform():
    department=request.form['department']
    sender=request.form['sender']
    receiver=request.form['receiver']
    amount=request.form['amount']
    print(department,sender,receiver,amount)
    contract,web3=connect_blockchain_fund(0)
    tx_hash=contract.functions.createfund(sender,receiver,int(amount)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(render_template('allocatefund.html',res='Fund Allocated'))

if __name__=="__main__":
    app.run(debug=True)
