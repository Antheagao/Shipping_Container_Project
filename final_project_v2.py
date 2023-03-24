from collections import defaultdict
from collections import deque
import heapq
import copy
import time

import pandas as pd
import numpy as np

from objects import Container, Ship, Operation

       
def main():
    # Declare variables
    file_name = ''
    B_ROWS = 4
    B_COLS = 24
    S_ROWS = 8
    S_COLS = 12
    bay = [[Container('', 0) for i in range(S_COLS)] for j in range(S_ROWS)]
    buffer = [[Container('', 0) for i in range(B_COLS)] for j in range(B_ROWS)]
    
    # Get the manifest file from the user
    '''file_name = str(input('Enter the name of the manifest file: '))'''
    file_name = 'ShipCase1.txt'
    
    # Read the manifest file into a dataframe
    manifest = pd.read_csv(file_name, sep=',', header=None, 
                           names=['X', 'Y', 'Weight', 'Name'])
    df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Name'])
    
    # Clean the dataframe
    clean_df(df)
    print(df)
    
    # Build the 2d table to represent the ship
    build_ship(bay, S_ROWS, S_COLS, df)
    
    # Balance the ship
    ship = Ship(bay, '', 0)
    begin_balance_test(ship, S_COLS)
    time1 = time.perf_counter()
    operations = a_star(ship, df, manifest)
    time2 = time.perf_counter()
    print('Time: ', '{:.3f}'.format(time2 - time1), 'seconds')
    '''for operation in operations:
        print(operation.move, operation.index, operation.x,
              operation.y, operation.name, operation.position)
        print()'''
    
    # Create the updated manifest file
    '''update_manifest(file_name, manifest)'''


''' Function to change weight to int and remove whitespace from name '''
def clean_df(df : pd.DataFrame) -> None:
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df['Weight'] = df['Weight'].astype('int32')
    
    # Convert the Name column to string values and remove whitespace
    df['Name'] = df['Name'].astype("string")
    df['Name'] = df['Name'].str.strip()
    

''' Function to build the ship table from the dataframe as a 2d list '''
def build_ship(ship : list[list[Container]], S_ROWS : int, S_COLS : int,
               df : pd.DataFrame) -> None:
    # Declare variables
    count = 0
    
    # Build the ship table from the dataframe
    for row in reversed(range(S_ROWS)):
        for col in range(S_COLS):
            ship[row][col].weight = df['Weight'][count]
            if df['Name'][count] == 'NAN':
                ship[row][col].name = '+++'
            elif df['Name'][count] == 'UNUSED':
                ship[row][col].name = '   '
            else:
                ship[row][col].name = df['Name'][count]
            count += 1


''' Function to print the ship table with formatting and bars '''
def print_table(ship : list[list[Container]], COLS : int) -> None:
    # Declare variables
    WIDTH = 3
    
    # Print the ship table with formatting and bars
    for row in range(COLS * WIDTH * 2 + 1):
        print('-', end='')
    print()
    for row in ship:
        for col in row:
            print('| ', col.name[0:WIDTH].ljust(WIDTH), sep='', end=' ')
        print('|')
        for row in range(COLS * WIDTH * 2 + 1):
            print('-', end='')
        print()
                

''' Function to perform a search to find the balanced state of the ship '''
def a_star(start : Ship, df : pd.DataFrame, manifest : pd.DataFrame) -> None:
    # Declare variables
    S_ROWS = len(start.bay)
    S_COLS = len(start.bay[0])
    can_drop_off = False
    open_set = []
    states = []
    seen = set()
    heapq.heappush(open_set, start)
    came_from = {}
    start_hash = (start.get_hash(), start.last_held)
    g_score = defaultdict(lambda: float('inf'))
    g_score[start_hash] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start_hash] = heuristic(start)
    
    # Find the shortest path to a balanced ship if it exists
    while len(open_set) > 0:
        ship = heapq.heappop(open_set)
        ship_hash = (ship.get_hash(), ship.last_held)
        seen.add(ship_hash)
        if ship.is_balanced():
            end_balance_test(ship, S_COLS)
            return create_path(came_from, ship_hash, df)

        # Check if the ship is in a state where it can pick up or drop off
        if can_drop_off == False:
            states = expand_pick_up(ship, seen, S_ROWS, S_COLS)
            can_drop_off = True
        else:
            states = expand_drop_off(ship, seen, S_ROWS, S_COLS)
            can_drop_off = False
        for state in states:
            neighbor_hash = (state.get_hash(), state.last_held)
            temp_g_score = g_score[ship_hash] + state.cost
            if temp_g_score < g_score[neighbor_hash]:
                came_from[neighbor_hash] = ship_hash
                g_score[neighbor_hash] = temp_g_score
                f_score[neighbor_hash] = temp_g_score + heuristic(state)
                if neighbor_hash not in open_set:
                    heapq.heappush(open_set, state)
                    
    # Ship cannot be balanced, perform SIFT
    return 'failure'


''' Function to build path of operators to balance the ship '''
def create_path(came_from : dict, current : tuple[str, str], 
                df: pd.DataFrame) -> list[Operation]:
    # Declare variables
    bay_states = deque(current)
    containers_held = deque()
    operations = []
    pick_up = True
    
    # Create the path of states from start to finish
    while current in came_from:
        current = came_from[current]
        bay_states.appendleft(current[0])
        containers_held.appendleft(current[1])
    
    # Get the operations for the operator
    containers_held.append(containers_held[len(containers_held) - 1])
    for index in range(1, len(bay_states) - 1): 
        hashed_words = get_hashed_words(bay_states[index])
        operation = Operation('', 0, 0, 0, '', '')
        false_index = hashed_words.index(containers_held[index])
        operation.x = false_index // 12
        operation.y = false_index % 12
        operation.index = (8 - 1 - operation.x) * 12 + operation.y
        operation.name = containers_held[index]
        operation.position = str(df.iloc[operation.index]['X']) + ',' + \
                             str(df.iloc[operation.index]['Y'])
        
        if pick_up == True:
            operation.move = 'Move '
            operations.append(operation)
            pick_up = False
        else:
            operation.move = 'To '
            operations.append(operation)
            pick_up = True
            
    # Return the operations 
    return operations


''' Function to calculate the heuristic value of a ship state '''
def heuristic(ship : Ship) -> int:
    # Declare variables
    S_COLS = len(ship.bay[0])
    left_kg = ship.get_left_kg()
    right_kg = ship.get_right_kg()
    balance_mass = 0
    deficit = 0
    masses = []
    h_n = 0
    items = []
    
    # Use left and right weight to calculate the balance mass and deficit
    balance_mass = (left_kg + right_kg) / 2 
    deficit = balance_mass - min(left_kg, right_kg)
    
    # Make a list of the masses on the smaller side of the ship
    if min(left_kg, right_kg) == right_kg:
        masses = ship.get_left_containers()
    else:
        masses = ship.get_right_containers()
    
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


''' Function to expand the state of the ship when picking up containers '''
def expand_pick_up(ship : Ship, seen : set, 
                   S_ROWS : int, S_COLS : int) -> list[Ship]:
    # Declare variables
    states = []
    cost = 0
    
    # Store the state of top containers that can be picked up in each column
    for col in range(S_COLS):
        for row in range(S_ROWS):
            bay = copy.deepcopy(ship.bay)
            hold = bay[row][col].name
            if hold == '+++' or hold == '   ' or str((bay, hold)) in seen:
                continue
            else:
                # Calculate the cost and store the ship
                cost = abs(-1 - row) + abs(0 - col)
                states.append(Ship(bay, hold, cost))
                break
    return states
               

''' Function to expand the state of the ship when dropping off containers '''
def expand_drop_off(ship : Ship, seen : set,
                    S_ROWS : int, S_COLS : int) -> list[Ship]:
    # Declare variables
    states = []
    
    # Store the state of containers that can be dropped off in top empty cells
    for col in range(S_COLS):
        for row in reversed(range(S_ROWS)):
            bay = copy.deepcopy(ship.bay)
            hold = bay[row][col].name
            if hold == ship.last_held:
                break
            if hold == '+++' or hold != '   ' or str((bay, hold)) in seen:
                continue
            else:
                # Get the coordinates of the last held container
                x, y = ship.get_coordinates(ship.last_held)
                
                # Swap the last held container with the empty cell
                bay[row][col], bay[x][y] = bay[x][y], bay[row][col]
                
                # Calculate the cost of the new state
                cost_to_top = abs(x - -1) 
                cost = cost_to_top + abs(-1 - row) + abs(y - col)
                
                # Create the new ship
                states.append(Ship(bay, ship.last_held, cost))
                break
    return states
                

''' Function to create a new manifest file once job has been completed '''   
def update_manifest(file_name : str, manifest : pd.DataFrame) -> None:
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)


''' Function to parse the manifest index from the hashed table '''
def parse_manifest_index(hashed_table : str, name : str) -> int:
    # Declare variables
    word_count = 0
    
    # Find the index of the word in the hashed table
    for i in range(len(hashed_table) - 2):
        if hashed_table[i] == ';':
            word_count += 1
            
        if hashed_table[i] == name[0] and \
           hashed_table[i + 1] == name[1] and \
           hashed_table[i + 2] == name[2]:
            return word_count
        

''' Function to parse the hashed table into a list of words '''
def get_hashed_words(table : str) -> list[str]:
    # Declare variables
    words = []
    word = ''
    
    # Get the words from the hashed table
    for i in range(len(table)):
        if table[i] == '-':
            words.append(word)
            word = ''
            
        if table[i] == ' ':
            word += table[i]
            
        if table[i].isalpha() or table[i] == '+':
            word += table[i]
    
    return words


''' Function to print the hashed table with bracket formatting '''
def print_hash_as_table(words : list[str]) -> None:
    # Declare variables
    num_bars = 73
    
    # Print the hashed table
    for index in range(len(words)):
        if index % 12 == 0:
            print()
            print('-' * num_bars)
            print('|', end=' ')
            
        print(words[index], end=' | ')
        
    print()
    print('-' * num_bars)


''' Function to print the start of the balance test '''
def begin_balance_test(ship: Ship, S_COLS: int) -> None:
    print('Original Ship')
    print_table(ship.bay, S_COLS)
    print('left weight: ', ship.get_left_kg(),
          'right weight: ',ship.get_right_kg())
    

''' Function to print the end of the balance test '''   
def end_balance_test(ship: Ship, S_COLS: int) -> None:
    print('Balanced Ship')
    print_table(ship.bay, S_COLS)
    print('left weight: ', ship.get_left_kg(),
          'right weight: ',ship.get_right_kg())
    

if __name__ == '__main__':
    main()