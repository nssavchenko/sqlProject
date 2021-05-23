import dbManipulator
import pandas as pd

df = pd.DataFrame(columns=['cash_and_due_from_banks', 'interest_income', 'non_interest_income', 'other_earning_assets', 'total_assets', 'total_deposits', 'total_equity', 'total_interest_expense', 'net_loans', 'net_interest_income', 'year', 'currency', 'country'])

#че-то запихваешь туда

dbManipulator(RIC, df)

#должно появится сообщение "успешно" если все норм или, что такой банк уже есть