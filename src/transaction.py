import random

random.seed(0)


def make_transaction(max_value=5):
    # This will create valid transactions in the range of (1,maxValue)
    sign = int(random.getrandbits(1)) * 2 - 1  # This will randomly choose -1 or 1
    amount = random.randint(1, max_value)
    alice_pays = sign * amount
    bob_pays = -1 * alice_pays
    # By construction, this will always return transactions that respect the conservation of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    return {u'Alice': alice_pays, u'Bob': bob_pays}


def is_valid_txn(txn, state):
    # Assume that the transaction is a dictionary keyed by account names

    # Check that the sum of the deposits and withdrawals is 0
    if sum(txn.values()) != 0:
        return False

    # Check that the transaction does not cause an overdraft
    # print(state)
    all_users = [*state]
    # print(all_users)
    for key in txn.keys():
        if key in all_users:
            acct_balance = state[key]
        else:
            acct_balance = 0
        if (acct_balance + txn[key]) < 0:
            return False

    return True
