from pybudget import app, ALLOWED_EXTENSIONS
from flask import render_template, request, redirect, url_for, flash
from pybudget.helpers import get_summaries
from pybudget.api_helpers import valid_transaction_entry
from pybudget.Transactions import add_api_transaction


@app.route('/')
@app.route('/budget')
def budget():
    summaries = get_summaries('1219')
    return render_template('budget.html', summaries=summaries)


@app.route('/transactions')
def transactions():
    return render_template('transactions.html')


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
