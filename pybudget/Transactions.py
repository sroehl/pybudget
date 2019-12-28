import re

import sqlalchemy.exc

from pybudget.DB import Transactions, EXPENSE, INCOME, get_session
from pybudget.api_helpers import valid_transaction_entry
from pybudget.Budget import get_rules


def get_transactions(month, category=None, flow=None):
    session = get_session()
    query = session.query(Transactions).filter(Transactions.month == month)
    if category is not None:
        query = query.filter(Transactions.category == category)
    if flow is not None:
        query = query.filter(Transactions.flow == flow)
    transactions = []
    for row in query.all():
        dict_item = row.__dict__
        transaction = {'date': dict_item['date'],
                       'name': dict_item['vendor'],
                       'category': dict_item['category'],
                       'amount': dict_item['amount'],
                       'id': dict_item['id']}
        transactions.append(transaction)
    return transactions


def get_totals(month, category, flow):
    session = get_session()
    if flow != EXPENSE and flow != INCOME:
        raise ValueError('Flow should be {} or {}'.format(EXPENSE, INCOME))
    query = session.query(Transactions.category, Transactions.amount).filter(Transactions.month == month, Transactions.flow == flow)
    if category is not None:
        query = query.filter(Transactions.category == category)
    query.group_by(Transactions.category)
    totals = {}
    for item in query.all():
        cat = item[0]
        if cat == '':
            cat = 'Uncategorized'
        if cat not in totals:
            totals[cat] = 0
        totals[cat] += item[1]
    return totals


def get_expense_totals(month, category=None):
    session = get_session()
    return get_totals(month, category, EXPENSE)


def get_income_totals(month, category=None):
    session = get_session()
    return get_totals(month, category, INCOME)


def remove_transaction(id):
    session = get_session()
    transaction_query = session.query(Transactions).filter(Transactions.id == id)
    if transaction_query.count() == 0:
        raise KeyError('{} was not found!'.format(id))
    transaction = transaction_query.all()[0]
    session.delete(transaction)
    return True


def refresh_transactions(month):
    rules = get_rules()
    session = get_session()
    query = session.query(Transactions).filter(Transactions.month == month)
    for row in query.all():
        dict_row = row.__dict__
        for rule in rules:
            print("checking {} against {}".format(dict_row['vendor'], rule['regex']))
            if re.match(rule['regex'], str.lower(dict_row['vendor'])):
                print("updating {} to category {}".format(dict_row['vendor'], rule['category']))
                row.category = rule['category']
                break
    session.commit()


def add_imported_transaction(date, month, vendor, amount, category, session, flow=EXPENSE):
    transaction = Transactions(date=date, month=month, imported_vendor=vendor, amount=amount, flow=flow,
                               category=category)
    session.add(transaction)
    session.commit()


def add_api_transaction(json):
    session = get_session()
    added = 0
    invalid = 0
    for entry in json:
        if valid_transaction_entry(entry):
            if 'month' not in entry:
                entry['month'] = entry['date'][0:2] + entry['date'][8:10]
            if 'notes' not in entry:
                entry['notes'] = ''
            if 'category' not in entry:
                entry['category'] = ''

            transaction = Transactions(date=entry['date'],
                                       month=entry['month'],
                                       vendor=entry['vendor'],
                                       amount=entry['amount'],
                                       notes=entry['notes'],
                                       flow=entry['flow'],
                                       category=entry['category'])
            session.add(transaction)
        else:
            invalid += 1
        try:
            session.commit()
            added += 1
        except sqlalchemy.exc.OperationalError as ex:
            print(ex)
            added = -1
        except sqlalchemy.exc.IntegrityError as ex:
            # TODO: This should be optimized to so we aren't getting new sessions all of the time
            session = get_session()
            print(ex)
    return added, invalid
