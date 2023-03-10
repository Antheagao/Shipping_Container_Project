import pandas as pd
import numpy as np

num = 0
df = pd.read_csv('ShipCase1.txt', sep=' ', header=None, names=['Coord', 'Weight', 'Container'])
#print(df)

df["Weight"] = df['Weight'].str.replace('{|}', '')
print(df)

#num = "90099"
df['Weight'] = df['Weight'].astype("string")
df['Weight'] = '{' + df['Weight'] + '}'
print(df)