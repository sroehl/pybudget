from pybudget import app
from flask import render_template
from pybudget.helpers import get_summaries


@app.route('/')
@app.route('/budget')
def budget():
    summaries = get_summaries('1219')
    return render_template('budget.html', summaries=summaries)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
