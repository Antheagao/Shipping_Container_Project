import pandas as pd
import numpy as np
from collections import defaultdict
import heapq


def main():
    # Declare variables
    file_name = ''
    B_ROWS = 4
    B_COLS = 24
    S_ROWS = 8
    S_COLS = 12
    ship = [['0' for i in range(S_COLS)] for j in range(S_ROWS)]
    buffer = [['   ' for i in range(B_COLS)] for j in range(B_ROWS)]
    
    # Get the manifest file from the user
    file_name = str(input('Enter the name of the manifest file: '))
    
    # Read the manifest file into a dataframe
    manifest = pd.read_csv(file_name, sep=',', header=None, 
                           names=['X', 'Y', 'Weight', 'Info'])
    df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    
    # Clean the dataframe
    clean_df(df)
    
    # Build the 2d table to represent the ship
    build_ship(ship, S_ROWS, S_COLS, df)
    
    # Create the updated manifest file
    update_manifest(file_name, manifest)


def clean_df(df : pd.DataFrame) -> None:
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df['Weight'] = df['Weight'].astype('int32')
    
    # Convert the info column to string values and remove whitespace
    df['Info'] = df['Info'].astype("string")
    df['Info'] = df['Info'].str.strip()
    

def build_ship(ship : list[list[str]], S_ROWS : int, S_COLS : int,
               df : pd.DataFrame) -> None:
    # Declare variables
    count = 0
    
    # Build the ship table from the dataframe
    for row in reversed(range(S_ROWS)):
        for col in range(S_COLS):
            if df['Info'][count] == 'NAN':
                ship[row][col] = '+++'
            elif df['Info'][count] == 'UNUSED':
                ship[row][col] = '   '
            else:
                ship[row][col] = df['Info'][count]
            count += 1


def print_table(ship : list[list[str]], COLS : int) -> None:
    # Declare variables
    COL_WIDTH = 3
    
    # Print the ship table with formatting and bars
    print_bars(COLS, COL_WIDTH)
    for row in ship:
        for col in row:
            print('| ', col[0:COL_WIDTH].ljust(COL_WIDTH), sep='', end=' ')
        print('|')
        print_bars(COLS, COL_WIDTH)


def print_bars(COLS : int, COL_WIDTH : int) -> None:
    # Print bars to divide the ship table into sections
    for row in range(COLS * COL_WIDTH * 2 + 1):
        print('-', end='')
    print()


def is_balanced(ship : list[list[str]], S_ROWS : int, S_COLS : int,
                df : pd.DataFrame) -> bool:
    # Declare variables
    left_kg = 0.0
    right_kg = 0.0
    weight_index = 0.0
    
    # Sum the weight of both sides of the ship and divide min by max weight
    for row in range(S_ROWS):
        for col in range(S_COLS):
            weight_index = (S_ROWS - 1 - row) * S_COLS + col
            if ship[row][col] == '+++' or ship[row][col] == '   ':
                continue
            elif (col < S_COLS // 2):
                left_kg += df.iloc[weight_index]['Weight']
            else:
                right_kg += df.iloc[weight_index]['Weight']

    # Return true if the weight is balanced and false if not
    return min(left_kg, right_kg) / max(left_kg, right_kg) > 0.9
                

def a_star(start : list[list[str]], df : pd.DataFrame,
           manifest : pd.DataFrame) -> None:
    # Declare variables
    S_ROWS = len(start)
    S_COLS = len(start[0])
    open_set = []
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = heuristic(start, df)
    
    while len(open_set) > 0:
        current = heapq.heappop(open_set)
        if is_balanced(current, S_ROWS, S_COLS, df):
            return reconstruct_path(came_from, current)
        for child in expand_state(current, S_ROWS, S_COLS):
            tentative_g_score = g_score[current] + distance(current, child)
            if tentative_g_score < g_score[child]:
                came_from[child] = current
                g_score[child] = tentative_g_score
                f_score[child] = tentative_g_score + heuristic(child, df)
                if child not in open_set:
                    heapq.heappush(open_set, child)
 
 
def reconstruct_path(came_from : dict,
                     current : list[list[str]]) -> list[list[str]]:
    num = 0
 
 
def heuristic(ship : list[list[str]], df : pd.DataFrame) -> int:
    num = 0


def expand_state(ship : list[list[str]],
                 S_ROWS : int, S_COLS : int) -> list[list[str]]:
    num = 0    
    
    
def update_manifest(file_name : str, manifest : pd.DataFrame) -> None:
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)


main()