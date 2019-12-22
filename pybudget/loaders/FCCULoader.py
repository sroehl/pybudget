from pybudget.loaders.Loader import  Loader
from pybudget.DB import EXPENSE, INCOME
import sys


class FCCULoader(Loader):

    # Format of CSV:
    # 0: Account
    # 1: Date
    # 2: Serial number
    # 3: Description
    # 4: Amount
    # 5: CR/DR

    @staticmethod
    def fix_line(line):
        chars = list(line)
        first_quote = False
        for i in range(0, len(chars)):
            if first_quote and line[i] == '"':
                first_quote = False
            elif line[i] == '"':
                first_quote = True
            if first_quote and line[i] == ',':
                chars[i] = ' '
        return ''.join(chars)

    def read_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if 'Account Designator' in line:
                    continue  # This is the header
                line = FCCULoader.fix_line(line.strip())
                vals = line.split(',')
                transaction = [vals[1], vals[3], vals[4], EXPENSE]
                if vals[5] == 'CR':
                    transaction[3] = INCOME
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
    fccu = FCCULoader(sys.argv[1], url)
    fccu.run()
