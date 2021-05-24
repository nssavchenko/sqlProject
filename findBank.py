import dbManipulator

RIC = 'SBER.MM'

df = dbManipulator.findBank(RIC)
print(df)
#получаешь датафрейм со всем дерьмом для camel или сообщение, что такого банка нет
#columns = ['total_equity', 'total_assets', 'total_loans', 'interes_income', 'non_interes_income', 'net_income', 'cash_and_due_from_banks', 'year']

