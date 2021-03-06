import psycopg2
import pandas as pd
from random import randint

COLUMNS = ['total_equity', 'total_assets', 'net_loans', 'interest_income', 'non_interest_income', 'net_income', 'cash_and_due_from_banks', 'year', 'cid']


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
        #print('Такой банк уже есть в базе данных')
        pass
    else:
        query = f"INSERT INTO general_info VALUES('{RIC}', '{df.iloc[0]['bank_name']}', '{df.iloc[0]['country']}');"
        cursor.execute(query)
    
    query = f"SELECT * FROM balance_sheet WHERE ric= '{RIC}' AND year = {df.iloc[0]['year']};"
    cursor.execute(query)

    if cursor.fetchone() is not None:
        return False

    query = "SELECT * FROM currency;"
    cursor.execute(query)
    result = cursor.fetchall()

    currency_id = give_id(result, 1, df.iloc[0]['currency'], 0)
    if currency_id[1] == 0:
        query = f"INSERT INTO currency VALUES({currency_id[0]}, '{df.iloc[0]['currency']}');"
        cursor.execute(query)
    
    query = f"INSERT INTO balance_sheet VALUES('{RIC}', {df.iloc[0]['cash_and_due_from_banks']}, {df.iloc[0]['net_loans']}, {df.iloc[0]['other_earning_assets']}, {df.iloc[0]['total_assets']}, {df.iloc[0]['total_deposits']}, {df.iloc[0]['total_equity']}, {df.iloc[0]['year']}, {currency_id[0]});"
    cursor.execute(query)

    query = f"INSERT INTO income_statement VALUES('{RIC}', {df.iloc[0]['interest_income']}, {df.iloc[0]['net_income']}, {df.iloc[0]['non_interest_income']}, {df.iloc[0]['year']}, {currency_id[0]});"
    cursor.execute(query)

    conn.commit()
    return True

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
        query  = f"SELECT b.total_equity, b.total_assets, b.net_loans, i.interest_income, i.non_interest_income, i.net_income, b.cash_and_due_from_banks, b.year, b.currency_id FROM balance_sheet as b JOIN income_statement as i on b.ric = i.ric AND b.year = i.year WHERE b.ric='{RIC}';"
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

def getGeneral(RIC):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT ric, bank_name, country_name FROM general_info WHERE ric='{RIC}'"
    cursor.execute(query)
    return cursor.fetchall()

def getCurrency(cid):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT currency_name FROM currency WHERE currency_id='{cid}'"
    cursor.execute(query)
    return cursor.fetchall()


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
    return

def updateBank(RIC, df):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"UPDATE balance_sheet SET cash_and_due_from_banks = {df.iloc[0]['cash_and_due_from_banks']}, net_loans = {df.iloc[0]['net_loans']}, other_earning_assets = {df.iloc[0]['other_earning_assets']}, total_assets = {df.iloc[0]['total_assets']}, total_deposits = {df.iloc[0]['total_deposits']}, total_equity = {df.iloc[0]['total_equity']}, year = {df.iloc[0]['year']} WHERE ric = '{RIC}';"
    cursor.execute(query)
    query = f"UPDATE income_statement SET interest_income = {df.iloc[0]['interest_income']}, net_income = {df.iloc[0]['net_income']}, non_interest_income = {df.iloc[0]['non_interest_income']}, year = {df.iloc[0]['year']} WHERE ric = '{RIC}';"
    cursor.execute(query)
    conn.commit()
    return

#Возращает тру если банк есть, фолс иначе то есть тебе нужно сначала эту функцию вызвать, и в зависимосте от ответа делать дальше
def checkCountry(country_name):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT country_name FROM countries WHERE country_name = '{country_name}';"
    cursor.execute(query)
    ans = cursor.fetchone()
    if ans is None:
        return False
    return True

def getCountryInfo(country_name):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT * FROM countries_info WHERE country_name = '{country_name}';"
    print(query)
    cursor.execute(query)
    ans = cursor.fetchall()
    return ans

def addCountry(df):
    #тут надо дф со столбцами 'country_name', 'currency_name'
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"INSERT INTO countries VALUES('{df.iloc[0]['country_name']}', '{df.iloc[0]['currency_name']}');"
    cursor.execute(query)
    conn.commit()
    return

def addCountryInfo(df):
    #тут надо дф со столбцами 'country_name', 'population', 'gdp', 'external_debt', 'year'
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"INSERT INTO countries_info VALUES('{df.iloc[0]['country_name']}', {df.iloc[0]['gdp']}, {df.iloc[0]['external_debt']}, {df.iloc[0]['population']}, {df.iloc[0]['year']});"
    print(query)
    cursor.execute(query)
    conn.commit()
    return

#тут функция смотрит есть ли уже такая пара валют
#сли есть то она апдейтит цену, если нет то добавлет новую пару и цену
def addCurrencyPair(df):
    #тут надо дф со стобцами 'currency1_name', 'currency2_name', 'currency_price'
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT * FROM currency_pairs WHERE currency1_name = '{df.iloc[0]['currency1_name']}' AND currency2_name = '{df.iloc[0]['currency2_name']}';"
    cursor.execute(query)
    ans = cursor.fetchone()

    if ans is not None:
        query = f"UPDATE currency_pairs SET currency_price = {df.iloc[0]['currency_price']} WHERE currency1_name = '{df.iloc[0]['currency1_name']}' AND currency2_name = '{df.iloc[0]['currency2_name']}';"
    else:
        query = f"INSERT INTO currency_pairs VALUES('{df.iloc[0]['currency1_name']}', '{df.iloc[0]['currency2_name']}', {df.iloc[0]['currency_price']});"
    cursor.execute(query)
    conn.commit()
    return

def getCurrencyPair(cur1, cur2):
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = f"SELECT * FROM currency_pairs WHERE currency1_name = '{cur1}' AND currency2_name = '{cur2}';"
    cursor.execute(query)
    ans = cursor.fetchone()
    return ans

'''
def fix();
    conn = psycopg2.connect(dbname='banks', user='postgres', password='ybrbnf00', host='localhost')
    cursor = conn.cursor()
    query = "ALTER TABLE income_statement RENAME COLUMN net_interest_income to net_income;"
    cursor.execute(query)
    conn.commit()
    return
'''    
