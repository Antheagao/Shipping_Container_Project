import pandas as pd
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
                           names=['X', 'Y', 'Weight', 'Name'])
    df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Name'])
    
    # Clean the dataframe
    clean_df(df)
    print(df)
    
    # Build the 2d table to represent the ship
    build_ship(ship, S_ROWS, S_COLS, df)
    '''a_star(ship, df, manifest)'''
    
    # Create the updated manifest file
    '''update_manifest(file_name, manifest)'''


def clean_df(df : pd.DataFrame) -> None:
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df['Weight'] = df['Weight'].astype('int32')
    
    # Convert the Name column to string values and remove whitespace
    df['Name'] = df['Name'].astype("string")
    df['Name'] = df['Name'].str.strip()
    

def build_ship(ship : list[list[str]], S_ROWS : int, S_COLS : int,
               df : pd.DataFrame) -> None:
    # Declare variables
    count = 0
    
    # Build the ship table from the dataframe
    for row in reversed(range(S_ROWS)):
        for col in range(S_COLS):
            if df['Name'][count] == 'NAN':
                ship[row][col] = '+++'
            elif df['Name'][count] == 'UNUSED':
                ship[row][col] = '   '
            else:
                ship[row][col] = df['Name'][count]
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
    manifest_index = 0
    
    # Sum the weight of both sides of the ship and divide min by max weight
    for row in range(S_ROWS):
        for col in range(S_COLS):
            manifest_index = (S_ROWS - 1 - row) * S_COLS + col
            if ship[row][col] == '+++' or ship[row][col] == '   ':
                continue
            elif (col < S_COLS // 2):
                left_kg += df.iloc[manifest_index]['Weight']
            else:
                right_kg += df.iloc[manifest_index]['Weight']

    # Return true if the weight is balanced and false if not
    return min(left_kg, right_kg) / max(left_kg, right_kg) > 0.9
                

def a_star(start : list[list[str]], df : pd.DataFrame,
           manifest : pd.DataFrame) -> None:
    # Declare variables
    S_ROWS = len(start)
    S_COLS = len(start[0])
    can_drop_off = False
    open_set = []
    states = []
    visited = []
    heapq.heappush(open_set, (start, ''))
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = heuristic(start, df)
    
    # Find the shortest path to a balanced ship if it exists
    while len(open_set) > 0:
        current = heapq.heappop(open_set)
        visited.append(current)
        if is_balanced(current, S_ROWS, S_COLS, df):
            return reconstruct_path(came_from, current)
        
        # Check if the ship is in a state where it can pick up or drop off
        if can_drop_off == False:
            states = expand_pick_up(current, df, visited, S_ROWS, S_COLS)
            for state in states:
                print_table(state, S_COLS)
            exit()
            can_drop_off = True
        else:
            states = expand_drop_off(current, df, visited, S_ROWS, S_COLS)
            can_drop_off = False
        for state in states:
            tentative_g_score = g_score[current] + distance(current, state)
            if tentative_g_score < g_score[state]:
                came_from[state] = current
                g_score[state] = tentative_g_score
                f_score[state] = tentative_g_score + heuristic(state, df)
                if state not in open_set:
                    heapq.heappush(open_set, state)
                    
    # Ship cannot be balanced, perform SIFT
    return "failure"
 
 
def reconstruct_path(came_from : dict,
                     current : list[list[str]]) -> list[list[str]]:
    num = 0
 
 
def heuristic(ship : list[list[str]], df : pd.DataFrame) -> int:
    num = 0
    

def distance():
    num = 0


def expand_pick_up(ship : tuple[list[list[str]], str], 
                   df : pd.DataFrame, 
                   visited : list[tuple[list[list[str]], str]],
                   S_ROWS : int,
                   S_COLS : int) -> list[tuple[list[list[str]]], str]:
    # Declare variables
    states = []
    state = ()
    
    # Store the top containers that can be picked up in each column
    for col in range(S_COLS):
        for row in range(S_ROWS):
            manifest_index = (S_ROWS - 1 - row) * S_COLS + col
            state = (ship, df.iloc[manifest_index]['Name'])
            if state[1] == 'NAN' or state[1] == 'UNUSED' or state in visited:
                continue
            else:
                states.append(state)
                break
    return states
               
    
def expand_drop_off(ship : list[list[str]], df : pd.DataFrame, visited : set,
                    S_ROWS : int, S_COLS : int) -> list[list[str]]:
    num = 0     
    
    
def update_manifest(file_name : str, manifest : pd.DataFrame) -> None:
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)


main()