import pandas as pd
import numpy as np
from collections import defaultdict
import heapq
import copy


class Ship:
    def __init__(self, bay: list[list[str]], last_held: str, cost: int):
        self.bay = bay
        self.last_held = last_held
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost
        

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
    
    # Balance the ship
    print(a_star(ship, df, manifest))
    
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
    seen = set()
    ship = Ship(start, '', 0)
    heapq.heappush(open_set, ship)
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[str((ship.bay, ship.last_held))] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[str((ship.bay, ship.last_held))] = heuristic(ship, df)
    
    # Find the shortest path to a balanced ship if it exists
    while len(open_set) > 0:
        current = heapq.heappop(open_set)
        seen.add(str((ship.bay, ship.last_held)))
        if is_balanced(ship.bay, S_ROWS, S_COLS, df):
            return reconstruct_path(came_from, str((ship.bay, ship.last_held)))

        # Check if the ship is in a state where it can pick up or drop off
        if can_drop_off == False:
            states = expand_pick_up(current, df, seen, S_ROWS, S_COLS)
            can_drop_off = True
        else:
            states = expand_drop_off(current, df, seen, S_ROWS, S_COLS)
            can_drop_off = False
        for state in states:
            current_hash = str((current.bay, current.last_held))
            neighbor_hash = str((state.bay, state.last_held))
            temp_g_score = g_score[current_hash] + state.cost
            if temp_g_score < g_score[neighbor_hash]:
                came_from[neighbor_hash] = current_hash
                g_score[neighbor_hash] = temp_g_score
                f_score[neighbor_hash] = temp_g_score + heuristic(state, df)
                if state not in open_set:
                    heapq.heappush(open_set, state)
                    
    # Ship cannot be balanced, perform SIFT
    return 'failure'
 
 
def reconstruct_path(came_from : dict, current : str) -> list[str]:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.prepend(current)
    return total_path
 
 
def heuristic(ship : Ship, df : pd.DataFrame) -> int:
    # Declare variables
    S_ROWS = len(ship.bay)
    S_COLS = len(ship.bay[0])
    left_kg = 0.0
    right_kg = 0.0
    manifest_index = 0
    balance_mass = 0
    deficit = 0
    masses = []
    h_n = 0
    items = []
    
    # Use left and right weight to calculate the balance mass and deficit
    for row in range(S_ROWS):
        for col in range(S_COLS):
            manifest_index = (S_ROWS - 1 - row) * S_COLS + col
            if ship.bay[row][col] == '+++' or ship.bay[row][col] == '   ':
                continue
            elif (col < S_COLS // 2):
                left_kg += df.iloc[manifest_index]['Weight']
            else:
                right_kg += df.iloc[manifest_index]['Weight']
    balance_mass = (left_kg + right_kg) / 2 
    deficit = balance_mass - min(left_kg, right_kg)
    
    # Make a list of the masses on the smaller side of the ship
    if min(left_kg, right_kg) == right_kg:
        for row in range(S_ROWS):
            for col in range(S_COLS // 2):
                if ship.bay[row][col] == '+++' or ship.bay[row][col] == '   ':
                    continue
                manifest_index = (S_ROWS - 1 - row) * S_COLS + col
                name = df.iloc[manifest_index]['Weight']
                temp = (ship.bay[row][col], name, col)
                masses.append(temp)
    else:
        for row in range(S_ROWS):
            for col in range(S_COLS // 2, S_COLS):
                if ship.bay[row][col] == '+++' or ship.bay[row][col] == '   ':
                    continue
                manifest_index = (S_ROWS - 1 - row) * S_COLS + col
                name = df.iloc[manifest_index]['Weight']
                temp = (ship.bay[row][col], name, col)
                masses.append(temp)
    
    # Sort the masses in decending order by weight
    masses = sorted(masses, key=lambda x: x[1], reverse=True)
    
    # Find the number of containers that need to be moved for balance
    for mass in masses:
        if mass[1] > deficit:
            continue
        else:
            deficit -= mass[1]
            items.append(mass)
    
    # Calculate the nearest column on the other side for each container  
    for item in items:
        if item[2] < S_COLS // 2:
            h_n += abs(S_COLS // 2 - item[2])
        else:
            h_n += abs(S_COLS // 2 - 1 - item[2])
    
    return h_n


def expand_pick_up(ship : Ship, df : pd.DataFrame, seen : set, 
                   S_ROWS : int, S_COLS : int) -> list[Ship]:
    # Declare variables
    states = []
    state = ()
    cost = 0
    
    # Store the state of top containers that can be picked up in each column
    for col in range(S_COLS):
        for row in range(S_ROWS):
            manifest_index = (S_ROWS - 1 - row) * S_COLS + col
            temp_ship = copy.deepcopy(ship.bay)
            state = (temp_ship, df.iloc[manifest_index]['Name'])
            if state[1] == 'NAN' or state[1] == 'UNUSED' or str(state) in seen:
                continue
            else:
                cost = abs(-1 - row) + abs(0 - col)
                new_ship = Ship(state[0], state[1], cost)
                states.append(new_ship)
                break
    return states
               
    
def expand_drop_off(ship : Ship, df : pd.DataFrame, seen : set,
                    S_ROWS : int, S_COLS : int) -> list[Ship]:
    # Declare variables
    states = []
    state = ()
    
    # Store the state of containers that can be dropped off in top empty cells
    for col in range(S_COLS):
        for row in reversed(range(S_ROWS)):
            manifest_index = (S_ROWS - 1 - row) * S_COLS + col
            temp_ship = copy.deepcopy(ship.bay)
            state = (temp_ship, df.iloc[manifest_index]['Name'])
            if state[1] == ship.last_held:
                break
            if state[1] == 'NAN' or state[1] != 'UNUSED' or str(state) in seen:
                continue
            else:
                move = np.argwhere(np.array(state[0]) == ship.last_held)
                x = move[0][0]
                y = move[0][1]
                state[0][row][col], state[0][x][y] = \
                    state[0][x][y], state[0][row][col]
                cost_to_top = abs(x - -1) 
                cost = cost_to_top + abs(-1 - row) + abs(y - col)
                new_ship = Ship(state[0], ship.last_held, cost)
                states.append(new_ship)
                break
    return states
                
     
def update_manifest(file_name : str, manifest : pd.DataFrame) -> None:
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)
    

main()