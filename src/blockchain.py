import json
import sys
import copy

from block import hash_me, make_block, checkBlockHash, checkBlockValidity
from state import updateState
from transaction import make_transaction, is_valid_txn


def checkChain(chain):
    # Work through the chain from the genesis block (which gets special treatment),
    #  checking that all transactions are internally valid,
    #    that the transactions do not cause an overdraft,
    #    and that the blocks are linked by their hashes.
    # This returns the state as a dictionary of accounts and balances,
    #   or returns False if an error was detected

    ## Data input processing: Make sure that our chain is a list of dicts
    if type(chain) == str:
        try:
            chain = json.loads(chain)
            assert (type(chain) == list)
        except:  # This is a catch-all, admittedly crude
            return False
    elif type(chain) != list:
        return False

    state = {}
    ## Prime the pump by checking the genesis block
    # We want to check the following conditions:
    # - Each of the transactions are valid updates to the system state
    # - Block hash is valid for the block contents

    for txn in chain[0]['contents']['txns']:
        state = updateState(txn, state)
    checkBlockHash(chain[0])
    parent = chain[0]

    ## Checking subsequent blocks: These additionally need to check
    #    - the reference to the parent block's hash
    #    - the validity of the block number
    for block in chain[1:]:
        state = checkBlockValidity(block, parent, state)
        parent = block

    return state


"""
txn -> map of <name, number>
block = {
  hash : string
  contents : {
    blockNumber: int
    parentHash: string
    txnCount: int
    txns: [txn]
}
"""
txnBuffer = [make_transaction() for i in range(30)]

# print(txnBuffer)

state = {u'Alice': 50, u'Bob': 50}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber': 0, u'parentHash': None, u'txnCount': 1, u'txns': genesisBlockTxns}
genesisHash = hash_me(genesisBlockContents)
genesisBlock = {u'hash': genesisHash, u'contents': genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]

blockSizeLimit = 5  # Arbitrary number of transactions per block-
#  this is chosen by the block miner, and can vary between blocks!

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)

    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = is_valid_txn(newTxn, state)

        if validTxn:
            txnList.append(newTxn)
            state = updateState(newTxn, state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on

    myBlock = make_block(txnList, chain)
    chain.append(myBlock)

print(chain[1])
print(checkChain(chain))
# chainAsText = json.dumps(chain, sort_keys=True)
# checkChain(chainAsText)

nodeBchain = copy.copy(chain)
nodeBtxns = [make_transaction() for i in range(5)]
newBlock = make_block(nodeBtxns, nodeBchain)

try:
    state = checkBlockValidity(newBlock, chain[-1], state)
    chain.append(newBlock)
except:
    print("Invalid block; ignoring and waiting for the next block...")

print("Blockchain on Node A is now %s blocks long" % len(chain))
