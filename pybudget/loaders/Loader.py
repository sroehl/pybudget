from pybudget.Transactions import get_transactions, add_imported_transaction
from pybudget.DB import get_session
from pybudget.helpers import get_category

class Loader:

    @staticmethod
    def in_transactions(date, name, amount, transactions):
        for transaction in transactions:
            if date == transaction.date and name == transaction.imported_vendor and amount == transaction.amount:
                return True
        return False

    def add_to_transactions(self):
        if len(self.transactions) == 0:
            return
        month = self.transactions[0][0][0:2] + self.transactions[0][0][8:10]
        db_transactions = get_transactions(month)
        session = get_session()
        for transaction in self.transactions:
            date, vendor, amount, flow = transaction
            if not Loader.in_transactions(date, vendor, amount, db_transactions):
                category = get_category(vendor, session)
                add_imported_transaction(date, month, vendor, amount, category, session, flow=flow)

    def __init__(self):
        self.transactions = []
