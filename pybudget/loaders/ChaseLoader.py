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

    def __init__(self, filename, url):
        Loader.__init__(self, url)
        self.filename = filename
        self.read_file()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        url = sys.argv[2]
    else:
        url = 'http://192.168.0.109:5000'
    chase = ChaseLoader(sys.argv[1], url)
    chase.run()
