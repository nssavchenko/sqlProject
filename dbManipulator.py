import psycopg2
import pandas as pd
from random import randint

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
        return 'Такой банк уже есть в базе данных'
    query = "SELECT * FROM general_info;"
    cursor.execute(query)
    result = cursor.fetchall()

    country_id = give_id(result, 3, df.iloc[0]['country'], 2)[0]
    query = f"INSERT INTO general_info VALUES('{RIC}', '{df.iloc[0]['bank_name']}', {country_id}, '{df.iloc[0]['country']}');"
    cursor.execute(query)

    query = "SELECT * FROM currency;"
    cursor.execute(query)
    result = cursor.fetchall()

    currency_id = give_id(result, 1, df.iloc[0]['currency'], 0)
    if currency_id[1] == 0:
        query = f"INSERT INTO currency VALUES({currency_id[0]}, '{df.iloc[0]['currency']}');"
        cursor.execute(query)
    
    query = "SELECT * FROM balance_sheet;"
    cursor.execute(query)
    result = cursor.fetchall()

    balance_sheet_id = generate_id(result, 0)
    query = f"INSERT INTO balance_sheet VALUES({balance_sheet_id[0]}, '{RIC}', {df.iloc[0]['cash_and_due_from_banks']}, {df.iloc[0]['net_loans']}, {df.iloc[0]['other_earning_assets']}, {df.iloc[0]['total_assets']}, {df.iloc[0]['total_deposits']}, {df.iloc[0]['total_equity']}, {df.iloc[0]['year']}, {currency_id[0]});"
    cursor.execute(query)

    query = 'SELECT * FROM income_statement'
    cursor.execute(query)
    result = cursor.fetchall()

    income_statement_id = generate_id(result, 0)
    query = f"INSERT INTO income_statement VALUES({income_statement_id[0]}, '{RIC}', {df.iloc[0]['interest_income']}, {df.iloc[0]['net_interest_income']}, {df.iloc[0]['non_interest_income']}, {df.iloc[0]['total_interest_expense']}, {df.iloc[0]['year']}, {currency_id[0]});"
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
        columns = ['total_equity', 'total_assets', 'total_loans', 'interes_income', 'non_interes_income', 'net_income', 'cash_and_due_from_banks', 'year']
        query  = f"SELECT b.total_equity, b.total_assets, b.net_loans, i.interest_income, i.non_interest_income, i.net_interest_income, b.cash_and_due_from_banks, b.year FROM balance_sheet as b JOIN income_statement as i on b.ric = i.ric WHERE b.ric='{RIC}';"
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            list(i)
        df = pd.DataFrame(result, columns=columns)
    return df

def findRICByName(name):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT ric, bank_name FROM general_info WHERE LOWER(bank_name) LIKE '%{name.lower()}%'"
    cursor.execute(query)
    return cursor.fetchall()

