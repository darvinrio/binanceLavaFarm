from web3 import Web3
import json
import keys
import abi
import time
import private

wallet = private.myWalletAddress
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

if(web3.isConnected()):
    print("connected")
else:
    print('not connected')
    exit()

lavaFi = web3.eth.contract(address=keys.lavacakeFinance, abi=abi.lavacakeFinance)

lavaToken = web3.eth.contract(address=keys.lavaToken, abi=abi.lavaToken)

swap = web3.eth.contract(address=keys.pancakeswap, abi=abi.pancakeswap)

lavaFiBal = lavaFi.functions.pendingLava(keys.btcb_pid, wallet).call()

lavaFiValue = web3.fromWei(lavaFiBal, 'ether')
print("lava Value = "+str(lavaFiValue))

blockNumber = web3.eth.block_number
while blockNumber  < 8435000 :
    print("not now cause its block number "+ str(blockNumber))
    blockNumber = web3.eth.block_number

print('here we go')

# harvest lavaToken

harvest = lavaFi.functions.deposit(keys.btcb_pid, 0).buildTransaction({
    'from' : wallet,
    'gasPrice' : web3.toWei('5','gwei'),
    'nonce' : web3.eth.get_transaction_count(wallet)
})

signed_txn = web3.eth.account.sign_transaction(harvest, private_key=private.key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Harvest Lava: " + web3.toHex(tx_token))

# approve lavaToken
lavaTokenBal = lavaToken.functions.balanceOf(wallet).call()
lavaBal = web3.fromWei(lavaTokenBal, 'ether')

start = time.time()

approve = lavaToken.functions.approve(keys.pancakeswap, lavaBal).buildTransaction({
            'from': wallet,
            'gasPrice': web3.toWei('5','gwei'),
            'nonce': web3.eth.get_transaction_count(wallet),
            })

signed_txn = web3.eth.account.sign_transaction(approve, private_key=private.key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Approved Lava: " + web3.toHex(tx_token))

time.sleep(10) #wait for approval

minBNB = 0.35
minOut = web3.toWei(minBNB,'ether')

# swap lavaToken 
swapLava = swap.functions.swapExactTokensForETH(lavaToken, minOut, [keys.lavaToken, keys.wbnbToken], wallet, (int(time.time()) + 1000000)).buildTransaction({
    'from' : wallet,
    'gasPrice' : web3.toWei('5', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet),
})

signed_txn = web3.eth.account.sign_transaction(swapLava, private_key=private.key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Swap completed " + web3.toHex(tx_token))