import pandas as pd
import numpy as np
import heapq

def main():
    # Declare variables
    file_name = ''
    B_ROWS = 4
    B_COLS = 24
    S_ROWS = 8
    S_COLS = 12
    ship = [['0' for i in range(S_COLS)] for j in range(S_ROWS)]
    
    # Get the manifest file from the user
    file_name = str(input('Enter the name of the manif file: '))
    
    # Read the manifest file into a dataframe
    manifest = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    print(df)
    
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df = df.astype({'Weight': 'int32'})
    print(df)
    
    # Create the updated manifest file
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)


def print_ship(ship : list[list[str]], S_COLS : int) -> None:
    O_WIDTH = 3
    print_bars(S_COLS)
    for i in ship:
        for j in i:
            print('|', j[0:O_WIDTH].ljust(O_WIDTH), end=' ')
        print('|')
        print_bars(S_COLS)


def print_bars(S_COLS : int) -> None:
    for i in range(S_COLS * 6 + 1):
        print('-', end='')
    print()

main()