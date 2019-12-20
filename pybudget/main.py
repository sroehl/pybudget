from pybudget import DB, helpers
from pybudget.loaders.ChaseLoader import ChaseLoader
from pybudget.loaders.FCCULoader import FCCULoader

from pybudget import app

def test_budget(session):
    # My sample budget
    session.query(DB.Budget).delete()
    steve_budget = [['Paycheck', 4205.30, 1],
                    ['Groceries', 500.00],
                    ['Restaurants', 600.00],
                    ['Phone', 174.00],
                    ['Fun Money', 400.00],
                    ['Shopping', 500.00],
                    ['Gas', 235.00],
                    ['Vacation', 400.00],
                    ['Mortgage', 515.45],
                    ['Water', 75.00],
                    ['Power/Gas', 190.00],
                    ['Gym', 58.00],
                    ['Philio', 20.00],
                    ['Hulu', 2.00],
                    ['Netflix', 13.00],
                    ['Car Insurance', 100.00],
                    ['Home Insurance', 50.00],
                    ['Car loan', 372.85]
                    ]
    for item in steve_budget:
        temp_b = None
        if len(item) == 3:
            temp_b = DB.Budget(month='1219', name=item[0], amount=item[1], flow=item[2])
        else:
            temp_b = DB.Budget(month='1219', name=item[0], amount=item[1])
        session.add(temp_b)
    session.commit()


def test_transactions(session):
    #  My test transactions
    clear_transactions(session)
    transactions = [
        ['12/01/2019', '1219', 'Walmart', 9.99, '', DB.EXPENSE, 'Shopping'],
        ['12/08/2019', '1219', 'Paycheck', 1000, '', DB.INCOME, 'Paycheck'],
        ['12/05/2019', '1219', 'BP', 34.26, '', DB.EXPENSE, 'Gas']
    ]
    for item in transactions:
        temp_t = DB.Transactions(date=item[0], month=item[1], store=item[2], amount=item[3], notes=item[4], flow=item[5], category=item[6])
        session.add(temp_t)
    session.commit()


def clear_transactions(session):
    session.query(DB.Transactions).delete()

def test_category_rules(session):
    session.query(DB.CategoryRules).delete()
    rules = [
        ["DOLLYWOOD'S DM", 'Vacation'],
        ['AMZN Mktp US*', 'Shopping'],
        ['Amazon.com*', 'Shopping']
    ]
    for rule in rules:
        temp_r = DB.CategoryRules(name=rule[0], category=rule[1])
        session.add(temp_r)
    session.commit()

def test():
    session = DB.get_session()
    test_budget(session)
    clear_transactions(session)
    #test_transactions(session)
    test_category_rules(session)
    session.close()
    ChaseLoader('/home/steve/Downloads/cc/0609_1214.csv').add_to_transactions()
    ChaseLoader('/home/steve/Downloads/cc/6048_1214.csv').add_to_transactions()
    FCCULoader('/home/steve/Downloads/cc/fccu.csv').add_to_transactions()

    helpers.get_money_left('1219')


if __name__ == '__main__':
    #test()
    app.run(debug=True, host='0.0.0.0', port=5000)
