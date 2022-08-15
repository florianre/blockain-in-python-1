def updateState(txn, state):
    # Inputs: txn, state: dictionaries keyed with account names, holding numeric values for transfer amount (txn)
    # or account balance (state)
    # Returns: Updated state, with additional users added to state if necessary
    # NOTE: This does not validate the transaction- just updates the state!

    # If the transaction is valid, then update the state
    state = state.copy()  # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state