import pandas as pd
df = pd.read_csv('data/2021年12月09日_有刨開.txt',delimiter='\t')
df.columns = ['Time','index','None', 'CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8']
print(df)
df.to_excel('data/2021年12月09日_有刨開.xlsx')