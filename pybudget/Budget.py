from pybudget.DB import Budget, get_session, CategoryRules


def get_budget(month, category=None):
    session = get_session()
    query = session.query(Budget).filter(Budget.month == month)
    if category is not None:
        query = query.filter(Budget.name == category)
    return query.all()


def get_categories(month):
    session = get_session()
    results = session.query(Budget.name).filter(Budget.month == month).all()
    categories = []
    for row in results:
        categories.append(row[0])
    return categories


def add_rule(regex, category):
    try:
        session = get_session()
        regex = str.lower(regex)
        result = session.query(CategoryRules).filter(CategoryRules.name == regex).first()
        if result is None:
            rule = CategoryRules(name=str.lower(regex), category=category)
            session.add(rule)
        else:
            result.category = category
        session.commit()
        return True
    except Exception as ex:
        print(ex)
        # TODO: Make this more specific
        return False


def get_rules():
    session = get_session()
    results = session.query(CategoryRules).all()
    rules = []
    for row in results:
        rules.append({'regex': row.name, 'category': row.category})
    return rules
