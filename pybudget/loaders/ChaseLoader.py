from pybudget.loaders.Loader import Loader
from pybudget.DB import EXPENSE
import sys


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

    def __init__(self, filename, url, username, password):
        Loader.__init__(self, url, username, password)
        self.filename = filename
        self.username = username
        self.password = password
        self.read_file()


if __name__ == '__main__':
    username = None
    password = None
    if len(sys.argv) == 5:
        url = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        url = 'http://192.168.0.109:5000'
    chase = ChaseLoader(sys.argv[1], url, username, password)
    chase.run()
