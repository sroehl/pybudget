from datetime import datetime

from pybudget import app
from flask import render_template, request
from pybudget.helpers import get_summaries
from pybudget.Transactions import add_api_transaction, get_transactions


@app.route('/')
@app.route('/budget')
def budget():
    summaries = get_summaries('1219')
    return render_template('budget.html', summaries=summaries)


@app.route('/transactions')
def transactions():
    d = datetime.today()
    month = str(d.month) + str(d.year)[2:4]
    month_trans = get_transactions(month)
    return render_template('transactions.html', transactions=month_trans)


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/api/transactions', methods=['POST'])
def api_transactions():
    json = request.get_json(True)
    added, invalid = add_api_transaction(json)
    return_json = {'added': added, 'invalid': invalid}
    return return_json


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
