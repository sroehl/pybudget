from pybudget.DB import Budget, get_session


def get_budget(month, category=None):
    session = get_session()
    query = session.query(Budget).filter(Budget.month == month)
    if category is not None:
        query = query.filter(Budget.name == category)
    return query.all()


def get_categories(month):
    session = get_session()
    return session.query(Budget.name).filter(Budget.month == month).all()