from pybudget.loaders.Loader import Loader
from pybudget.DB import EXPENSE


class ChaseLoader(Loader):

    def read_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if 'Transaction Date' in line:
                    continue  # This is the header
                line = line.strip()
                vals = line.split(',')
                if vals[4] == 'Payment':
                    continue
                transaction = [vals[0], vals[2], float(vals[5]) * -1, EXPENSE]
                self.transactions.append(transaction)

    def __init__(self, filename):
        Loader.__init__(self)
        self.filename = filename
        self.read_file()
