import hashlib
import json
import sys

from py._xmlgen import unicode

from state import updateState
from transaction import is_valid_txn


def hash_me(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


def make_block(txns, chain):
    parent_block = chain[-1]  # last element
    parent_hash = parent_block[u'hash']
    block_number = parent_block[u'contents'][u'blockNumber'] + 1
    block_contents = {u'blockNumber': block_number, u'parentHash': parent_hash,
                      u'txnCount': len(txns), 'txns': txns}
    block_hash = hash_me(block_contents)
    block = {u'hash': block_hash, u'contents': block_contents}

    return block


def checkBlockHash(block):
    # Raise an exception if the hash does not match the block contents
    expectedHash = hash_me(block['contents'])
    if block['hash'] != expectedHash:
        raise Exception('Hash does not match contents of block %s' %
                        block['contents']['blockNumber'])
    return


def checkBlockValidity(block, parent, state):
    block_number = block['contents']['blockNumber']
    print(block_number)
    if block['contents']['parentHash'] != hash_me(parent['contents']):
        raise Exception('Parent hash not accurate at block %s' % block_number)

    checkBlockHash(block)

    if block_number - 1 != parent['contents']['blockNumber']:
        raise Exception('Hash does not match contents of block %s' % block_number)

    for txn in block['contents']['txns']:
        if is_valid_txn(txn, state):
            state = updateState(txn, state)
        else:
            raise Exception('Invalid transaction in block %s: %s' % (block_number, txn))

    return state