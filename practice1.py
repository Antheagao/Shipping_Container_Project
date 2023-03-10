# This file is used to try/test code 
import pandas as pd
import numpy as np

df = pd.read_csv('ShipCase1.txt', sep=' ', header=None, names=['Coord', 'Weight', 'Container'])
#print(df)

df["Weight"] = df['Weight'].str.replace('{|}', '')
print(df)

df['Weight'] = df['Weight'].astype("string")
df['Weight'] = '{' + df['Weight'] + '}'
print(df)

 # Remove the square brackets from the X and Y columns
df["X"] = df['X'].str.replace(r'[', '', regex=True)
df["Y"] = df['Y'].str.replace(r']', '', regex=True)
print(df)