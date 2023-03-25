from collections import defaultdict
from collections import deque
from datetime import datetime
import heapq
import copy
import time
import os

import pandas as pd

from objects3 import Container, Ship, Operation

       
def main():
    # Declare variables
    file_name = 'ship_cases/'
    log_file_name = 'KeoghLongBeach.txt'
    date_time = ''
    user_name = ''
    ship_name = ''
    confirm = ''
    job_type = ''
    running = True
    B_ROWS = 4
    B_COLS = 24
    S_ROWS = 8
    S_COLS = 12
    operations = []
    bay = [[Container('', 0) for i in range(S_COLS)] for j in range(S_ROWS)]
    buffer = [[Container('', 0) for i in range(B_COLS)] for j in range(B_ROWS)]
    
    # Get date and time values for the log file
    date_time = datetime.now().year
    log_file_name = log_file_name.replace('.txt', str(date_time) + '.txt')
    log_file = open(log_file_name, 'a')
        
    # Have the user sign in and get the manifest file
    user_name = str(input('Enter your name to sign in: '))
    date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
    log_file.write(date_time + user_name + ' signs in\n')
    
    # Loop the program until the user is done working
    while running:
        # Check if log file is still in the same year
        log_file_name = 'KeoghLongBeach.txt'
        date_time = datetime.now().year
        log_file_name = log_file_name.replace('.txt', str(date_time) + '.txt')
        log_file = open(log_file_name, 'a')
        
        # Get the manifest file from the user
        file_name = 'ship_cases/'
        file_name += str(input('Enter the name of the manifest file: '))
        ship_name = file_name.replace(".txt", "")
        ship_name = ship_name.replace("ship_cases/", "")
        
        # Read the manifest file into a dataframe
        manifest = pd.read_csv(file_name, sep=',', header=None, 
                               names=['X', 'Y', 'Weight', 'Name'])
        df = pd.read_csv(file_name, sep=',', header=None, 
                         names=['X', 'Y', 'Weight', 'Name'])
        
        # Clean the dataframe
        clean_df(df)
        print('\nThe manifest file you are working with:')
        print(df)
        
        # Build the 2d table to represent the ship
        build_ship(bay, S_ROWS, S_COLS, df)
        ship = Ship(bay, '', 0)
        date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
        log_file.write(date_time + 'Manifest ' +
                       file_name.replace("ship_cases/", "") + ' is opened, '
                       'there are ' + str(ship.get_container_count()) +
                       ' containers on the ship\n')
        print('\nThe ship you are working with:\t\t'
              'Container count:', ship.get_container_count())
        print_table(ship.bay, S_COLS)
        
        # Ask the user which job they are doing
        job_type = str(input('\nSelect the job type:\n(1). Balance\n'
                             '(2). Unload/Load\nEnter your choice: '))
        
        # Begin ship balancing/unloading/loading
        if job_type == '1':
            if ship.get_container_count() == 0:
                print('\nThere are no containers on the ship,'
                      ' please select another job type.\n')
                continue
            time1 = time.perf_counter()
            operations = a_star(ship, df)
            time2 = time.perf_counter()
            print('\nOperations calculated in'
                  ':', '{:.3f}'.format(time2 - time1), 'seconds\n')
            print('Estimated time to balance:',
                  calculate_time(operations), 'minutes\n')
            user_name = balancing(ship, operations,
                                  manifest, user_name,
                                  ship_name, log_file)
        else:
            begin_unload = None
            begin_load = None
        
        # Create the updated manifest file and send it to the ship captain
        update_manifest(file_name, manifest)
        file_name = file_name.replace(".txt", "OUTBOUND.txt")
        print('\n\nFinished a job cycle,',
              file_name.replace("ship_cases/", ""), 'was written to desktop.\n'
              'Send the updated manifest to the ship captain.\n')
        confirm = str(input('Enter (c) to confirm the message was read: '))
        while confirm != 'c':
            confirm = str(input('Enter (c) to confirm the message was read: '))
        date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
        log_file.write(date_time + 'Finished a Cycle. Manifest ' + 
                       file_name.replace("ship_cases/", "") + 
                       ' was written to desktop, and a reminder pop-up'
                       ' to operator to send file was displayed.\n')
        
        # Ask the user if they want to work on another ship
        user_input = str(input('Do you want to work on another ship? (y/n): '))
        if user_input == 'y':
            running = True
            user_input = str(input('Do you want to change user? (y/n): '))
            while user_input != 'y' and user_input != 'n':
                user_input = str(input('Do you want to change user? (y/n): '))
            if user_input == 'y':
                date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
                log_file.write(date_time + user_name + ' signs out\n')
                user_name = str(input('Enter your name to sign in: '))
                date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
                log_file.write(date_time + user_name + ' signs in\n')
        else:
            running = False
            
    # Write the user signing out to the log file
    date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
    log_file.write(date_time + user_name + ' signs out\n')
    log_file.close()


''' Function to change weight to int and remove whitespace from name '''
def clean_df(df: pd.DataFrame) -> None:
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df['Weight'] = df['Weight'].astype('int32')
    
    # Convert the Name column to string values and remove whitespace
    df['Name'] = df['Name'].astype("string")
    df['Name'] = df['Name'].str.strip()
    

''' Function to build the ship table from the dataframe as a 2d list '''
def build_ship(ship: list[list[Container]], S_ROWS: int, S_COLS: int,
               df: pd.DataFrame) -> None:
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
def print_table(ship: list[list[Container]], COLS: int) -> None:
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
def a_star(start: Ship, df: pd.DataFrame) -> list[Operation] or str:
    # Declare variables
    S_ROWS = len(start.bay)
    S_COLS = len(start.bay[0])
    can_pick_up = True
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
    while open_set:
        ship = heapq.heappop(open_set)
        ship_hash = (ship.get_hash(), ship.last_held)
        seen.add(ship_hash)
        if ship.is_balanced():
            return create_path(came_from, ship_hash, df)

        # Check if the ship is in a state where it can pick up or drop off
        if can_pick_up:
            states = expand_pick_up(ship, seen, S_ROWS, S_COLS)
            can_pick_up = False
        else:
            states = expand_drop_off(ship, seen, S_ROWS, S_COLS)
            can_pick_up = True
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
def create_path(came_from: dict, current: tuple[str, str], 
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
        operation = Operation('', 0, 0, 0, '   ', '')
        false_index = hashed_words.index(containers_held[index])
        operation.x = false_index // 12
        operation.y = false_index % 12
        operation.name = containers_held[index]
        operation.index = (8 - 1 - operation.x) * 12 + operation.y
        operation.position = str(df.iloc[operation.index]['X'])\
                             + ','\
                             + str(df.iloc[operation.index]['Y'])
        if pick_up == True:
            operation.move = 'Move '
            operations.append(operation)
            pick_up = False
        else:
            operation.move = 'To '
            operations.append(operation)
            pick_up = True
    return operations


''' Function to calculate the heuristic value of a ship state '''
def heuristic(ship: Ship) -> int:
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
def expand_pick_up(ship: Ship, seen: set, 
                   S_ROWS: int, S_COLS: int) -> list[Ship]:
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
def expand_drop_off(ship: Ship, seen: set,
                    S_ROWS: int, S_COLS: int) -> list[Ship]:
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
                
                # Calculate the cost of the new state and create the ship
                cost_to_top = abs(x - -1) 
                cost = cost_to_top + abs(-1 - row) + abs(y - col)
                states.append(Ship(bay, ship.last_held, cost))
                break
    return states
                

''' Function to create a new manifest file once job has been completed '''   
def update_manifest(file_name: str, manifest: pd.DataFrame) -> None:
    file_name = file_name.replace('ship_cases/', 'ship_cases_outbound/')
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manifest.to_csv(file_name, header=None, index=False)
    os_name = os.getlogin()
    desktop = 'C:\\Users\\' + os_name + '\\OneDrive\\Desktop\\' +\
              file_name.replace('ship_cases_outbound/', '')
    manifest.to_csv(desktop, header=None, index=False)
        

''' Function to parse the hashed table into a list of words '''
def get_hashed_words(table: str) -> list[str]:
    # Declare variables
    words = []
    word = ''
    
    # Get the words from the hashed table
    for index in range(len(table)):
        if table[index] == '-':
            words.append(word)
            word = ''    
        if table[index] == ' ':
            word += table[index] 
        if table[index].isalpha() or table[index] == '+':
            word += table[index]
    return words


''' Function to print the hashed table with bracket formatting '''
def print_hash_as_table(words: list[str]) -> None:
    # Declare variables
    NUM_BARS = 73
    
    # Print the hashed table
    for index in range(len(words)):
        if index % 12 == 0:
            print()
            print('-' * NUM_BARS)
            print('|', end=' ')
        print(words[index], end=' | ')
    print()
    print('-' * NUM_BARS)


''' Function to print the start of the balance test '''
def begin_balance_test(ship: Ship, S_COLS: int) -> None:
    print('\nShip you are working on:')
    print_table(ship.bay, S_COLS)
    print('left weight: ', ship.get_left_kg(),
          'right weight: ',ship.get_right_kg())
    

''' Function to print the end of the balance test '''   
def end_balance_test(ship: Ship, S_COLS: int) -> None:
    print('Balanced Ship')
    print_table(ship.bay, S_COLS)
    print('left weight: ', ship.get_left_kg(),
          'right weight: ',ship.get_right_kg())


''' Function to calculate the estimated time to balance the ship '''
def calculate_time(operations: list[Operation]) -> int:
    # Declare variables
    minutes = 0
    virtual_x = -1
    virtual_y = 0
    can_pickup = True
    last_position_y = 0
    
    # Calculate the estimated time to balance the ship in minutes
    for operation in operations:
        if can_pickup:
            minutes += abs(virtual_x - operation.x) +\
                       abs(virtual_y - operation.y) + abs(operation.x - -1)
            last_position_y = operation.y
            can_pickup = False
        else:
            minutes += abs(virtual_x - operation.x) +\
                       abs(last_position_y - operation.y)
            can_pickup = True
    return minutes


''' Function to print the ship name, operator name, and ship containers '''
def display_ship_status(ship: Ship, ship_name: str, user_name: str) -> None:
    S_COLS = len(ship.bay[0])
    print()
    print('Ship Name:', ship_name, '\t\tOperator:', user_name)
    print_table(ship.bay, S_COLS)
    print('Port weight:', ship.get_left_kg(),
          '\t\tStarboard weight:', ship.get_right_kg())
  

''' Function to let the operator perform the operations on the ship '''
def balancing(ship: Ship, operations: list[Operation],
              manifest: pd.DataFrame, user_name: str,
              ship_name: str, log_file: str) -> str:
    # Have the operator perform the operations on the ship
    print('<' * 23,'Begin balancing the ship', '>' * 23, '\n')
    for index in range(0, len(operations), 2):
        x1, y1 = operations[index].x, operations[index].y
        x2, y2 = operations[index + 1].x, operations[index + 1].y
        index1, index2 = operations[index].index, operations[index + 1].index
        print('=' * 22,
              operations[index].move, operations[index].position, '',
              operations[index + 1].move, operations[index + 1].position,
              '=' * 22)
        ship.bay[x2][y2].name = ' X '
        display_ship_status(ship, ship_name, user_name)
        ship.bay[x2][y2].name = '   '
        print()
        
        choice = input('Enter (1) to confirm the move, '
                       '(2) to switch user, or (3) to write an issue'
                       ' to the log file: ')
        while choice != '1' and choice != '2' and choice != '3':
            choice = input('Enter (1) to confirm the move, '
                       '(2) to switch user, or (3) to write an issue'
                       ' to the log file: ')
        if choice == '2':
            date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
            log_file.write(date_time + user_name + ' signs out\n')
            user_name = input('Enter your name to sign in: ')
            date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
            log_file.write(date_time + user_name + ' signs in\n')
            choice = input('Enter (1) to confirm the previous move: ')
            while choice != '1':
                choice = input('Enter (1) to confirm the previous move: ')
        elif choice == '3':
            date_time = datetime.now().strftime("%B %d %Y: %H:%M ")
            message = input('Enter the issue: ')
            log_file.write(date_time + message + '\n')
            choice = input('Enter (1) to confirm the previous move: ')
            while choice != '1':
                choice = input('Enter (1) to confirm the previous move: ')
        
        # Swap the containers in the ship bay and update the manifest
        ship.bay[x1][y1], ship.bay[x2][y2] = ship.bay[x2][y2], ship.bay[x1][y1]
        manifest.iloc[index1]['Name'], manifest.iloc[index2]['Name'] =\
            manifest.iloc[index2]['Name'], manifest.iloc[index1]['Name']
        manifest.iloc[index1]['Weight'], manifest.iloc[index2]['Weight'] =\
            manifest.iloc[index2]['Weight'], manifest.iloc[index1]['Weight']
        print()
    print('<' * 21,'Fininshed balancing the ship', '>' * 21, '\n')
    display_ship_status(ship, ship_name, user_name)
    return user_name


''' Function to load containers onto the ship'''
def loading(ship: Ship, df : pd.DataFrame, manifest : pd.DataFrame) -> None:
    # Enter the label of the container along with
    # the weight you want to give it
    load_containers = []
    load_weight = []
    final_coordinates = []

    print('Enter the label of the container you wish to load\n'
          'Press \'ENTER\' and then type the weight,'
          'click \'ENTER\' when done')
    print('If no more containers to load or not loading, press \'ENTER\''
          'without typing anything when asked for label of container')
    
    new_container = input("Enter container label: ")
    while new_container != '': # Empty string
        weightString = "Enter " + new_container + "\'s weight: "
        new_container_weight = input(weightString)
        load_containers.append(new_container)
        load_weight.append(new_container_weight)
        final_coordinates.append((-1,-1)) # Adds to the list each time as this
                                          # is our starting point each time
        new_container = input("Enter container name: ")
    #print(load_containers)
    #print(load_weight)

    if load_containers == 0:
        #no containers loading so we only unloaded
        return

    # Similar to unloading minMoves, 
    # except we keep track of moves per container
    # Find all open columns where we can move
    # Calc manhattan distance from 
    # Should do a while loop that goes through all load_containers list,
    # and after we load, we pop, only when we have an empty list 
    # do we stop loading process
    occupied_columns = []
    open_columns = []

    # Get a list of columns that have open slots to load my containers
    open_columns = ship.get_open_columns(occupied_columns) 
    orderOfMoves = [] # List of strings that state each operation that
                      # crane operator has to do, ex : Move (-1,-1) to (4,0)
    movesCoords = []  # Has all the coordinates moves 
    manhattan = 0  # Keeps track of total time, taken at the end

    if len(open_columns) == 0:
        #ship full
        print("Ship at max capacity to load, cannot proceed further")
        print("Add a comment about this")
        return

    # While our final coordinates is not empty...
    while len(final_coordinates) > 0: 
        row,column = final_coordinates[0]
        MinMoves = 10000
        minX,minY= (-1,-1)
        for openColLocation in open_columns:
            currMoves, currCords = ship.load((row, column),
                                             openColLocation,
                                             MinMoves)
            if currMoves < MinMoves:
                MinMoves = currMoves
                minX,minY = currCords
        move = "Move " + str((row, column)) + " to " + str((minX,minY))
        movesCoords.append((row, column))
        movesCoords.append((minX, minY))
        orderOfMoves.append(move)

        # Add container to table
        ship.bay[minX][minY].name = load_containers[0]
        
        # Do manifest manip HERE!!!!
        ship.bay[minX][minY].weight = load_weight[0]

        # Add total moves values from pink star to pick up truck here
        manhattan = manhattan + 2

        #get open columns again here
        open_columns = ship.get_open_columns(occupied_columns)
        #print_table(ship.bay, 12)
        final_coordinates.pop(0)
        load_containers.pop(0)
        load_weight.pop(0)

    # orderOfMoves stores a string of moves from container to container,
    # when switching containers, we must manipulate manifest
    #print(orderOfMoves)
    #print(movesCoords)
    for index, elem in enumerate(movesCoords):
        if (index<(len(movesCoords) - 1)):
            currX,currY = elem
            nextX,nextY = movesCoords[index + 1]
            manhattan = abs(currX - nextX) + abs(currY - nextY) + manhattan
        else:
            manhattan = manhattan

    #print(manhattan)
    return


''' Function to unload containers from the ship '''
def unloading(ship: Ship, df: pd.DataFrame, manifest: pd.DataFrame) -> None:
    # Get user input about which containers we are unloading
    # Empty array to collect containers we wish to unload
    unload_containers = [] 
    
    # Ask user to type container name, followed by enter to enter it
    # If done with typing, simply click enter with an empty string
    print('Enter the names of the containers you wish to unload\n'
          'If done entering container labels or not unloading, click \'ENTER\' without typing.')

    new_container = input("Enter container name: ")
    
    # While loop to keep iterating until user 
    # clicks 'ENTER' by itself (empty string)
    while new_container != "":
        # Add container names to array of unload_containers
        unload_containers.append(new_container)

        # Ask user to enter another container
        new_container = input("Enter container name: ")
    
    # Done collecting array of strings that container

    if len(unload_containers) == 0: #no containers inputted:
        return

    totalContainersOnShip = ship.get_container_count()
    if totalContainersOnShip == 0:
        print("Cannot unload any container since our ship is empty")
        print("Add comment to log about this.")
        return    
    # all containers we wish to unload
    seen_containers = set()
    uniq_containers = []

    for x in unload_containers:
        if x not in seen_containers:
            uniq_containers.append(x)
            seen_containers.add(x)

    seen_containers2 = set()
    dupes = []

    for x in unload_containers:
        if x in seen_containers2:
            dupes.append(x)
        else:
            seen_containers2.add(x)

    # Collecting an array that consists of unique containers and duplicates.
    # If dupes length == 0, then we have all unique containers,
    # else we must get multiple container coordinates that must be unique
    final_coordinates = []
    if len(dupes) == 0:
        # All containers are unique, check to see if multiple names
        # of the unique containers exists in manifest
        for i in uniq_containers:
            minList = []
            coordinates = []
            x, y = ship.get_coordinates(i)
            coordinates.append((x, y))
            coordinates= ship.get_uniq_coordinates(i, coordinates)
            for val in coordinates:
                row,column = val
                stackedCrates = ship.get_stacked((row,column))
                stackedCrates = stackedCrates +\
                                abs(row - -1) + abs(column - -1)
                minList.append(stackedCrates)
            finalXy = coordinates[minList.index(min(minList))]
            final_coordinates.append(finalXy)
        #print(final_coordinates)
    else: # Example, we want to unload "Cat", "Cat", "Dog". but 3 "Cats" exist
        # Not all containers are uniq, 
        for i in uniq_containers:
            minList = []
            coordinates = []
            x, y = ship.get_coordinates(i)
            coordinates.append((x, y))
            coordinates= ship.get_uniq_coordinates(i, coordinates)
            for val in coordinates:
                row, column = val
                stackedCrates = ship.get_stacked((row, column))
                # Calculates distance from drop off to unloading container 
                # + takesinto account amount of containers stacked on top of it
                stackedCrates = stackedCrates +\
                                abs(row - -1) + abs(column - -1) 
                minList.append(stackedCrates)
            finalXy = coordinates[minList.index(min(minList))]
            final_coordinates.append(finalXy)

            for j in dupes:
                if j == i:
                    # Removes minimum value from minList
                    minList.remove(min(minList)) 
                    coordinates.remove(finalXy) 
                    finalXy = coordinates[minList.index(min(minList))]
                    final_coordinates.append(finalXy)
    # Collected all coordinates we need for unloading, did checks for dupes,
    # and everything to get best coordinates available,
    #print(final_coordinates)

    occupied_columns = []
    open_columns = []

    for i, j in final_coordinates:
        occupied_columns.append(j)
    open_columns = ship.get_open_columns(occupied_columns)
    #print(occupied_columns)
    #print(open_columns)
    orderOfMoves = []
    totalMoves = 0
    movesCoords = []
    movesCoords.append((-1, -1))
    manhattan = 0

    # While our final coordinates is not empty...
    while len(final_coordinates) > 0: 
        # Get a list of the amount of crates that are stacked on top,
        # ideally,we want to start unloading the crate with the least
        # amount of crates stacked on
        finalStacked = []
        for i in final_coordinates:
            row,column = i
            stackedOnTop = ship.get_stacked((row,column))
            finalStacked.append(stackedOnTop)

        # Sort array in ascending order
        # Sort the parallel lists in ascending order given
        # the crates on top list as our key
        finalStacked, final_coordinates = (list(t) for t in zip(
                                *sorted(zip(finalStacked, final_coordinates)))) 
        #print(final_coordinates)
        #print(finalStacked)

        # Takes first value of list of crates stacked to see
        # if we are able to unload
        while finalStacked[0] > 0: 
            # Get the coordinate of the top-most 
            # container that we want to unload
            row,column = final_coordinates[0]
            row = row - finalStacked[0]  # Ex (7,8) -> (5,8) for owl test case
            LeftMinMoves = 10000
            LeftminX, LeftminY= (-1,-1)
            RightMinMoves = 10000
            RightminX, RightminY = (-1,-1)

            for openColLocation in open_columns:
                # If openColLocation is less than our current col,
                # we move left, up, and down
                # Else we move right, up, and down
                # Ee need to check if we are able to move left, if not move up,
                
                # If we move up and are out of bounds aka in -1,
                # then we move to openCol and keep going down until
                # we cant go further down
                
                # We should save two values, names currMoves and currCords,
                # as well with minMoves and minCords
                if openColLocation < column: # Line 229 column value
                    #print(open_columns)
                    currMoves, currCords = ship.move_left((row, column),
                                                          openColLocation,
                                                          LeftMinMoves)
                    #print(currMoves)
                    #print(currCords)
                    if currMoves < LeftMinMoves:
                        LeftMinMoves = currMoves
                        LeftminX,LeftminY = currCords
                else: # Cases for when we move right and up
                    currMoves, currCords = ship.move_right((row, column),
                                                            openColLocation,
                                                            RightMinMoves)
                    if currMoves < RightMinMoves:
                        RightMinMoves = currMoves
                        RightminX,RightminY = currCords

            # At the end
            finalStacked[0] = finalStacked[0] - 1
            if LeftMinMoves < RightMinMoves:
                smolCoordX, smolCoordY = LeftminX,LeftminY
                move = "Move " + str((row, column)) + " to " +\
                        str((LeftminX, LeftminY))
                movesCoords.append((row, column))
                movesCoords.append((LeftminX, LeftminY))
                totalMoves = totalMoves + LeftMinMoves
                orderOfMoves.append(move)
            else:
                smolCoordX, smolCoordY = RightminX,RightminY
                move = "Move " + str((row, column)) + " to " +\
                        str((RightminX, RightminY))
                movesCoords.append((row, column))
                movesCoords.append((RightminX, RightminY))
                totalMoves = totalMoves + RightMinMoves
                orderOfMoves.append(move)

            # Switch containers here
            ship.bay[row][column], ship.bay[smolCoordX][smolCoordY] =\
            ship.bay[smolCoordX][smolCoordY], ship.bay[row][column]
            # Do manifest manip HERE !!!!

        row, column = final_coordinates[0]
        totalMoves = totalMoves + abs(row - -1) + abs(column - -1)
        move = "Move " + str(final_coordinates[0]) + " to (-1, -1)" 
        movesCoords.append(final_coordinates[0])
        movesCoords.append((-1, -1))
        orderOfMoves.append(move)

        # Remove container from table
        ship.bay[row][column].name = '   '
        ship.bay[row][column].weight = 0     # Do manifest manip HERE !!!!

        # Add total moves values from pink star to pick up truck here
        manhattan = manhattan + 2

        # Remove column element from occupied list
        occupied_columns.remove(column)

        # Get open columns again here
        open_columns = ship.get_open_columns(occupied_columns)

        #print_table(ship.bay, 12)
        final_coordinates.pop(0)
        finalStacked.pop(0)

    #print(orderOfMoves)

    # orderOfMoves stores a string of moves from container to container,
    # when switching containers, we must manipulate manifest
    
    for index, elem in enumerate(movesCoords):
        if (index<(len(movesCoords)-1)):
            currX,currY = elem
            nextX,nextY = movesCoords[index+1]
            manhattan = abs(currX - nextX) + abs(currY - nextY) + manhattan
        else:
            manhattan = manhattan
    #print(manhattan)  
    return


if __name__ == '__main__':
    main()