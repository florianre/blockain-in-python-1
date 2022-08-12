import hashlib
import json
import sys
import random

from py._xmlgen import unicode


def hash_me(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


random.seed(0)


def makeTransaction(maxValue=5):
    # This will create valid transactions in the range of (1,maxValue)
    sign = int(random.getrandbits(1)) * 2 - 1  # This will randomly choose -1 or 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays
    # By construction, this will always return transactions that respect the conservation of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    return {u'Alice': alicePays, u'Bob': bobPays}


txnBuffer = [makeTransaction() for i in range(30)]

print(txnBuffer)
