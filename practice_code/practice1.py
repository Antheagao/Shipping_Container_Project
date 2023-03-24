# This file is used to try/test code 
import pandas as pd
import numpy as np
import heapq
from collections import defaultdict
from datetime import date 
from datetime import datetime

# Code to read the manifest file into a dataframe
'''df = pd.read_csv('ShipCase1.txt', sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
manif = pd.read_csv('ShipCase1.txt', sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
print(df)'''


# Code to remove curly braces from the weight column
'''df["Weight"] = df['Weight'].str.replace(r'{|}', '')'''


# Code to append backets to the weight column
'''df['Weight'] = df['Weight'].astype("string")
df['Weight'] = '{' + df['Weight'] + '}'''


 # Code to remove square brackets from data column
'''df["X"] = df['X'].str.replace(r'[', '', regex=True)
df["Y"] = df['Y'].str.replace(r']', '', regex=True)'''


# Code to update/create a manifest file
'''manif.to_csv('name', header=None, index=False)'''


# Code to swap two rows in the manifest file
'''manif.iloc[0], manif.iloc[1] = manif.iloc[1].copy(), manif.iloc[0].copy()'''


# Code to pass by reference, use a list  to pass by reference
'''def main():
    var = [1]
    sup(var)
    for i in var:
        print(i)

def sup(var : int) -> None:
    var[0] = 2
    
main()'''


# Code to print 2d list
'''ship = [['0' for i in range(12)] for j in range(8)]
for i in ship:
    for j in i:
        print(j, end=' ')
    print()'''
    

# Code to print 2d list in bracket format
'''ship = [[0 for i in range(12)] for j in range(8)]
for row in ship:
    print(row)'''

    
# Code to print 2d list with output formatting
'''ship = [['0' for i in range(12)] for j in range(8)]
ship[5][5] = 'DOG'
for i in range(12 * 6 + 1):
    print('-', end='')
print()
for i in ship:
    for j in i:
        print('|', j[0:3].ljust(3), end=' ')
    print('|')
    for i in range(12 * 6 + 1):
        print('-', end='')
    print()'''


# Code to access a specific element in a column of the dataframe
'''df = pd.read_csv('ShipCase1.txt', sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
print(df['Weight'][1])'''


# Code to access weight based on column number
'''df.iloc[2]['Weight']'''


# Code to use the min heap library
'''h = []
heapq.heappush(h, (4, "eat"))
heapq.heappush(h, (4, "dog"))
heapq.heappush(h, (4, "cat"))
heapq.heappush(h, (4, ""))
heapq.heappush(h, (4, "nat"))

while len(h) > 0:
    print(heapq.heappop(h))'''

# Code to print row in dataframe
'''print(df.iloc[0])'''

# code to access a specific element in a row of the dataframe
'''print(df.iloc[0]['Weight'])'''


# Code to add string of items to a set
'''seen = set()
item1 = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'dog')
item2 = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'cat')
item3 = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'dog')

temp = items[0]
print(temp)
temp = list(np.concatenate(temp).flat)
temp = str(temp) + ', ' + items[1]

seen.add(temp)
print(seen)
print(str(items))
seen.add(str(item1))
seen.add(str(item2))
print(seen)'''

# code to find index of a specific element in a list
'''items = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

move = np.argwhere(np.array(items) == 8)
print(move[0][0], move[0][1])'''

# Code to use a class for the ship bay
'''class Ship:
    def __init__(self, bay: list[list[str]], last_held: str, cost: int):
        self.bay = bay
        self.last_held = last_held
        self.cost = cost
        
ship = Ship ([['0' for i in range(12)] for j in range(8)], 'Dog', 0)
print(str((ship.bay, ship.last_held)))'''

# Code to iterate through right side of 2d list
'''table = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
for i in range(len(table)):
    for j in range(2, len(table[i])):
        print(table[i][j], end=' ')
    print()'''
    
'''table = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(table)
table = str(table)
print(table)
table = table.replace('[', '')'''

# code to swap manifest values
'''df = pd.read_csv('ship_cases/ShipCase1.txt', sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Name'])

df.iloc[0]['Name'], df.iloc[1]['Name'] = df.iloc[1]['Name'], df.iloc[0]['Name'] 
#df.iloc[0], df.iloc[1] = df.iloc[1].copy(), df.iloc[0].copy()
df.to_csv('ship_cases/ShipCase1.txt', header=None, index=False)'''

# code to get the current date and time
'''today = date.today()
print("Today's date:", today)
d2 = today.strftime("%B %d %Y")
print("d2 =", d2)

now = datetime.now()
print("now =", now)
dt_string = now.strftime("%B %d %Y: %H:%M")
print("date and time =", dt_string)
year = datetime.now().year
print(year)

date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
print(date_time)'''
log_file_name = 'KoughLongBeach.txt'
date_time = datetime.now().year
log_file_name = log_file_name.replace('.txt', str(date_time) + '.txt')
date_time = datetime.now().strftime("%B %d %Y: %H:%M")
log_file = open(log_file_name, 'a')