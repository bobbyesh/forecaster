from consttimes import START_TIME, START_MONTH, END_TIME, END_MONTH_YEAR
from month import Month
from income import Income
from housing import HomeOwned, Rental
from expense import Expenses
from tabulate import tabulate

INIT_SAVINGS = 1000


def get_expenses(current_time):
    home = Rental(1350, current_time)
    fixed = {Expenses.AUTO_INSURANCE: 72, Expenses.FOOD: 967, Expenses.GAS: 80, Expenses.OTHER: 500,
             Expenses.BUFFER: 300, }
    return Expenses(month=current_time, housing=home, fixed=fixed)


def get_income(current_time):
    changes = {
        0: {
            Month(2, 2019): 4350,
            Month(5, 2020): 7900,
        },
    }

    return Income(month=current_time, initial_incomes={0: 4050, 1: 1700}, changes=changes)


def as_months(anylist: list):
    for i in range(0, len(anylist), 12):
        yield anylist[i:i+12]


def get_tables():
    years = 3
    start_month = Month(4, 2018)
    end_month = Month(4, start_month.year + years)

    # Init total savings
    current_total = 0
    initial_savings = 1000

    # Init current time
    current_time = Month(4, 2018)

    # Initialize income and expenses
    income = get_income(current_time)
    expenses = get_expenses(current_time)

    months = []
    expenses_list = []
    incomes = []
    nets = []
    savings = []

    # Accumulate savings
    while expenses.month < end_month:
        monthly_net = income.monthly() - expenses.monthly()
        current_total += monthly_net

        months.append(expenses.month)
        expenses_list.append(expenses.monthly())
        incomes.append(income.monthly())
        nets.append(monthly_net)

        if savings:
            temp = savings[-1] + monthly_net
        else:
            temp = initial_savings

        savings.append(temp)

        expenses.increment_month()
        income.increment_month()

    month_chunks = list(as_months(months))
    expenses_chunks = list(as_months(expenses_list))
    income_chunks = list(as_months(incomes))
    net_chunks = list(as_months(nets))
    savings_chunks = list(as_months(savings))

    tables = []
    for m, e, i, n, s in zip(month_chunks, expenses_chunks, income_chunks, net_chunks, savings_chunks):
        t = [
            ['Month'] + m,
            ['Expenses'] + e,
            ['Income'] + i,
            ['Net'] + n,
            ['Savings'] + s
        ]
        tables.append(t)

    return tables


    print("By {} your savings will be {}".format(expenses.month, current_total))


tables = get_tables()

with open('table.html', 'w') as f:
    for t in tables:
        html = tabulate(t, tablefmt='html')
        f.write(html)