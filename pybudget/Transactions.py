import sqlalchemy.exc

from pybudget.DB import Transactions, EXPENSE, INCOME, get_session
from pybudget.api_helpers import valid_transaction_entry


def get_transactions(month, category=None, flow=None):
    session = get_session()
    query = session.query(Transactions).filter(Transactions.month == month)
    if category is not None:
        query = query.filter(Transactions.category == category)
    if flow is not None:
        query = query.filter(Transactions.flow == flow)
    return query.all()


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
        totals[item[0]] = item[1]
    return totals


def get_expense_totals(month, category=None):
    session = get_session()
    return get_totals(month, category, EXPENSE, session)


def get_income_totals(month, category=None):
    session = get_session()
    return get_totals(month, category, INCOME, session)


def remove_transaction(id):
    session = get_session()
    transaction_query = session.query(Transactions).filter(Transactions.id == id)
    if transaction_query.count() == 0:
        raise KeyError('{} was not found!'.format(id))
    transaction = transaction_query.all()[0]
    session.delete(transaction)
    return True


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
            # TODO: This should remove rows from added if they weren't added
            session = get_session()
            print(ex)
    return added, invalid
