import dbManipulator
import pandas as pd

columns=['cash_and_due_from_banks', 'interest_income', 'non_interest_income', 'other_earning_assets', 'total_assets', 'total_deposits', 'total_equity', 'total_interest_expense', 'net_loans', 'net_interest_income', 'year', 'currency', 'country', 'bank_name']

sample = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'test', 'test', 'test']

df = pd.DataFrame([sample], columns=columns)
print(dbManipulator.addBank('badc', df))

