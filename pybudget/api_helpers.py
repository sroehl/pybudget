






def valid_transaction_entry(entry):
    if 'date' not in entry:
        return False
    if 'vendor' not in entry:
        return False
    if 'amount' not in entry:
        return False
    if 'flow' not in entry:
        entry['flow'] = 0
    return True
