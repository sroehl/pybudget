from datetime import datetime

from pybudget import app
from flask import render_template, request, url_for, redirect, flash
from pybudget.helpers import get_summaries
from pybudget.Transactions import add_api_transaction, get_transactions, refresh_transactions
from pybudget.Budget import get_categories, add_rule


def get_month():
    d = datetime.today()
    return str(d.month) + str(d.year)[2:4]


@app.route('/')
@app.route('/budget')
def budget():
    summaries = get_summaries('1219')
    return render_template('budget.html', summaries=summaries)


@app.route('/transactions')
def transactions():
    month = get_month()
    refresh_transactions(month)
    month_trans = get_transactions(month)
    categories = get_categories(month)
    return render_template('transactions.html', transactions=month_trans, categories=categories)


@app.route('/rules', methods=['POST', 'GET'])
def rules():
    if request.method == 'POST':
        form_vals = request.form
        if 'vendorRegex' not in form_vals or 'category' not in form_vals:
            flash('Error adding rule')
            redirect(url_for('transactions'))
        added = add_rule(form_vals['vendorRegex'], form_vals['category'])
        refresh_transactions(get_month())
        if added:
            print("added rule: {} - {}".format(form_vals['vendorRegex'], form_vals['category']))
        else:
            print("Failed to add rule")
        redirect(url_for('transactions'))
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
