import requests


class Loader:

    def add_to_transactions(self):
        if len(self.transactions) == 0:
            return
        entries = []
        for transaction in self.transactions:
            date, vendor, amount, flow = transaction
            month = date[0:2] + date[8:10]
            entry = {'date': date,
                     'month': month,
                     'vendor': vendor,
                     'amount': amount,
                     'flow': flow
                     }
            entries.append(entry)
        r = requests.post(self.url, json=entries, auth=(self.username, self.password))
        print('Sent to server: {}'.format(r.status_code))
        if r.status_code == 200:
            print('Added: {}'.format(r.json()['added']))
            print('Invalid: {}'.format(r.json()['invalid']))

    def read_file(self):
        raise NotImplementedError('read_file not implemented')

    def run(self):
        self.read_file()
        self.add_to_transactions()

    def __init__(self, url, username, password):
        self.transactions = []
        self.username = username
        self.password = password
        self.url = url + '/api/transactions'
