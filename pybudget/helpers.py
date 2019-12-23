from pybudget.Transactions import get_totals
from pybudget.Budget import get_budget
from pybudget.DB import EXPENSE, INCOME, CategoryRules


def get_category(name, session):
    rules = {}
    for row in session.query(CategoryRules.name, CategoryRules.category).all():
        rules[row.name] = row.category
    for rule in rules:
        if rule in name:
            return rules[rule]
    return None


def get_money_left(month, category=None):
    budgets = get_budget(month, category=category)
    spents = get_totals(month, category, EXPENSE)
    mades = get_totals(month, category, INCOME)
    for budget in budgets:
        if budget.name in spents:
            print('{} left in {}'.format(round(budget.amount - spents[budget.name], 2), budget.name))
        if budget.name in mades:
            print('{} left to earn in {}'.format((budget.amount - mades[budget.name]), budget.name))


def get_summaries(month):
    budgets = get_budget(month)
    spents = get_totals(month, None, EXPENSE)
    mades = get_totals(month, None, INCOME)
    summary = {}
    for budget in budgets:
        if budget.name not in summary:
            summary[budget.name] = {'amount': budget.amount, 'flow': budget.flow}
        if budget.name in spents:
            summary[budget.name]['spent'] = spents[budget.name] * 1.0
            summary[budget.name]['left'] = budget.amount - spents[budget.name]
            summary[budget.name]['percent'] = round(spents[budget.name] / summary[budget.name]['amount'] * 100.0, 2)
        if budget.name in mades:
            summary[budget.name]['made'] = mades[budget.name] * 1.0
            summary[budget.name]['left'] = budget.amount - mades[budget.name]
            summary[budget.name]['percent'] = round(mades[budget.name] / summary[budget.name]['amount'] * 100.0, 2)
    return summary
