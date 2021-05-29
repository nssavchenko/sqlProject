import psycopg2
import pandas as pd
from random import randint

COLUMNS = ['total_equity', 'total_assets', 'net_loans', 'interest_income', 'non_interest_income', 'net_interest_income', 'cash_and_due_from_banks', 'year']


def generate_id(result, position):
    if result == []:
        return (randint(10000, 99999), 0)
    ids = []
    for i in result:
        ids.append(i[position])
        while True:
            id = randint(10000, 99999)
            if id not in ids:
                return (id, 0)

def give_id(result, position_name, name, position_id):
    if result == []:
        return (randint(10000, 99999), 0)
    for i in result:
        if name == i[position_name]:
            return (i[position_id], 1)
    return generate_id(result, position_id)

def addBank(RIC, df):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()

    query = f"SELECT * FROM general_info WHERE ric= '{RIC}';"
    cursor.execute(query)
    if cursor.fetchone() is not None:
        print('Такой банк уже есть в базе данных')
    else:
        query = "SELECT * FROM general_info;"
        cursor.execute(query)
        result = cursor.fetchall()

        country_id = give_id(result, 3, df.iloc[0]['country'], 2)[0]
        query = f"INSERT INTO general_info VALUES('{RIC}', '{df.iloc[0]['bank_name']}', {country_id}, '{df.iloc[0]['country']}');"
        print(query)
        cursor.execute(query)

    query = "SELECT * FROM currency;"
    cursor.execute(query)
    result = cursor.fetchall()

    currency_id = give_id(result, 1, df.iloc[0]['currency'], 0)
    if currency_id[1] == 0:
        query = f"INSERT INTO currency VALUES({currency_id[0]}, '{df.iloc[0]['currency']}');"
        cursor.execute(query)
    
    query = f"INSERT INTO balance_sheet VALUES('{RIC}', {df.iloc[0]['cash_and_due_from_banks']}, {df.iloc[0]['net_loans']}, {df.iloc[0]['other_earning_assets']}, {df.iloc[0]['total_assets']}, {df.iloc[0]['total_deposits']}, {df.iloc[0]['total_equity']}, {df.iloc[0]['year']}, {currency_id[0]});"
    cursor.execute(query)

    query = f"INSERT INTO income_statement VALUES('{RIC}', {df.iloc[0]['interest_income']}, {df.iloc[0]['net_interest_income']}, {df.iloc[0]['non_interest_income']}, {df.iloc[0]['total_interest_expense']}, {df.iloc[0]['year']}, {currency_id[0]});"
    cursor.execute(query)

    conn.commit()
    return 'Успешно'

def findBank(RIC):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT * FROM general_info WHERE ric='{RIC}';"
    cursor.execute(query)
    if cursor.fetchone() == None:
        return 'В базе данных нет такого банка'
    else:
        #query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'income_statement' LIMIT 3 OFFSET 2;"
        #cursor.execute(query)
        #column_names = list(cursor.fetchall())
        #query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'balance_sheet';"
        query  = f"SELECT b.total_equity, b.total_assets, b.net_loans, i.interest_income, i.non_interest_income, i.net_interest_income, b.cash_and_due_from_banks, b.year FROM balance_sheet as b JOIN income_statement as i on b.ric = i.ric AND b.year = i.year WHERE b.ric='{RIC}';"
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            list(i)
        df = pd.DataFrame(result, columns=COLUMNS)
    return df

"""
def getCurrency(RIC):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT * FROM general_info WHERE ric='{RIC}';"
"""

def findRICByName(name):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT ric, bank_name FROM general_info WHERE LOWER(bank_name) LIKE '%{name.lower()}%'"
    cursor.execute(query)
    return cursor.fetchall()

def removeBank(RIC):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"DELETE FROM income_statement WHERE ric = '{RIC}';"
    cursor.execute(query)
    query = f"DELETE FROM balance_sheet WHERE ric = '{RIC}';"
    cursor.execute(query)
    query = f"DELETE FROM general_info WHERE ric = '{RIC}';"
    cursor.execute(query)
    conn.commit()

def updateBank(RIC, df):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"UPDATE balance_sheet SET cash_and_due_from_banks = {df.iloc[0]['cash_and_due_from_banks']}, net_loans = {df.iloc[0]['net_loans']}, other_earning_assets = {df.iloc[0]['other_earning_assets']}, total_assets = {df.iloc[0]['total_assets']}, total_deposits = {df.iloc[0]['total_deposits']}, total_equity = {df.iloc[0]['total_equity']}, year = {df.iloc[0]['year']} WHERE ric = '{RIC}';"
    cursor.execute(query)
    query = f"UPDATE income_statement SET interest_income = {df.iloc[0]['interest_income']}, net_interest_income = {df.iloc[0]['net_interest_income']}, non_interest_income = {df.iloc[0]['non_interest_income']}, total_interest_expense = {df.iloc[0]['total_interest_expense']}, year = {df.iloc[0]['year']} WHERE ric = '{RIC}';"
    cursor.execute(query)
    conn.commit()