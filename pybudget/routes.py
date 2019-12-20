from pybudget import app, ALLOWED_EXTENSIONS
from flask import render_template, request, redirect, url_for, flash
from pybudget.helpers import get_summaries


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('File not in upload')
        return redirect(url_for('transactions'))
    file = request.files['file']
    bank = request.form.get('bank', None)
    if bank is None:
        flash('No bank!')
        return redirect(url_for('transactions'))
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('transactions'))
    if file and allowed_file(file.filename):
        file.sa



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
