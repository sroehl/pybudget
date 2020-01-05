from datetime import datetime

from pybudget import app
from flask import render_template, request, url_for, redirect, flash
from pybudget.helpers import get_summaries
from pybudget.Transactions import add_api_transaction, get_transactions, refresh_transactions
from pybudget.Budget import get_categories, add_rule


def get_month(subtract=0):
    d = datetime.today()
    month = d.month
    year = d.year
    if subtract > 0:
        year_sub = int(subtract / 12)
        month_sub = subtract % 12
        year = year - year_sub
        month = month - month_sub
        if month < 1:
            year = year - 1
            month = month + 12
    return str(month) + str(year)[2:4]


@app.route('/')
@app.route('/budget')
def budget():
    subtract = request.args.get('month', default=0, type=int)
    month = get_month(subtract)
    print("|{}|".format(month))
    summaries = get_summaries(month)
    return render_template('budget.html', summaries=summaries)


@app.route('/transactions')
def transactions():
    subtract = request.args.get('month', default=0, type=int)
    month = get_month(subtract)
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
