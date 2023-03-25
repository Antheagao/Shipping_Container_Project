''' Container class represents a container in the ship's bay.
    It has a name and a weight.
'''
class Container:
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight
        

''' Operation class represents an operation that can be performed on the ship.
    It has a move for pick up and drop off, index for the real dataframe 
    index of the manifest, x as the 2d table x position, y as the 2d table
    y position, name for the container name, and position for the [x,y] 
    coordinate in the manifest.
'''
class Operation:
    def __init__(self, move: str, index: int, x: int, y: int, name: str, 
                 position: str):
        self.move = move
        self.index = index
        self.x = x
        self.y = y
        self.name = name
        self.position = position


''' Ship class represents a ship in the simulation. It has a bay which holds
    a 2d table of containers, last_held for the last held container,
    and cost for movement between pick ups and drop offs.
'''
class Ship:
    def __init__(self, bay: list[list[Container]], last_held: str, cost: int):
        self.bay = bay
        self.last_held = last_held
        self.cost = cost
        
    def __lt__(self, other):
        return self.cost < other.cost
    
    def get_left_kg(self) -> float:
        left_kg = 0.0
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL // 2):
                    left_kg += self.bay[row][col].weight
        return left_kg
    
    def get_right_kg(self) -> float:
        right_kg = 0.0
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL // 2, COL):
                    right_kg += self.bay[row][col].weight
        return right_kg
    
    def is_balanced(self) -> bool:
        return min(self.get_left_kg(), self.get_right_kg()) / \
               max(self.get_left_kg(), self.get_right_kg()) > 0.9

    def get_left_containers(self) -> list[tuple[str, int, int]]:
        left_containers = []
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL // 2):
                name = self.bay[row][col].name
                weight = self.bay[row][col].weight
                left_containers.append((name, weight, col))
        return left_containers
    
    def get_right_containers(self) -> list[tuple[str, int, int]]:
        right_containers = []
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL // 2, COL):
                name = self.bay[row][col].name
                weight = self.bay[row][col].weight
                right_containers.append((name, weight, col))
        return right_containers
    
    def get_coordinates(self, container: str) -> tuple[int, int]:
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL):
                if self.bay[row][col].name == container:
                    return (row, col)
        return (-1, -1)

    def get_uniq_coordinates(self, container: str, coord: set) -> set:
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL):
                if self.bay[row][col].name == container and\
                   (row, col) not in coord:
                    x, y = (row, col)
                    coord.add((x, y))
        return coord

    def get_stacked(self, coords: tuple[int, int]) -> int:
        row,col = coords
        count = 0

        for x in reversed(range(row)):
            if self.bay[x][col].name != '   ':
                count = count + 1
            else:
                continue
        return count
        
    def get_hash(self):
        state_repr = ""
        for row in self.bay:
            for container in row:
                state_repr += f"{container.name}-{container.weight};"
        state_repr += self.last_held
        return state_repr
    
    def get_container_count(self) -> int:
        count = 0
        for row in self.bay:
            for container in row:
                if container.name != '   ' and container.name != '+++':
                    count += 1
        return count
    
    def get_open_columns(self, coord: list[int]) -> list[int]:
        ROW = len(self.bay)
        COL = len(self.bay[0])
        open = []
        
        for row in range(ROW):
            for col in range(COL):
                if self.bay[row][col].name == '   ' and (col) not in open:
                    x, y = (row,col)
                    if y not in coord:
                        open.append(y)
        return open
    
    def move_left(self, coord: tuple[int, int],
                  openColumn: int, minMoves: int) -> tuple[int, int, int]:
        movesAndCoord = []
        moves = 0
        MaxMoves = minMoves
        row, col = coord

        # Flag is true when we are at col == open Column 
        # and we have something to sit on
        for columns in reversed(range(col)): # Goes from column 8 to 0
            # I am able to move to the left
            if self.bay[row][columns].name == '   ': 
                # Set our curr col to be the backwards iterations
                col = columns
                moves = moves + 1
            # Im in the outta bounds region right now,
            elif row == -1 and col != openColumn:
                col = columns
                moves = moves + 1
            # I cant move left so i move up
            elif self.bay[row][columns].name != '   ':  
                # While i cant go left and I can still keep moving up
                while row != 0: 
                    row = row - 1
                    moves = moves + 1
                    # Means that I can move left without going outta bounds
                    if row != 0 and self.bay[row][columns].name == '   ':
                        col = columns
                        moves = moves + 1
                        break
            if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1, -1))
                return movesAndCoord
            # I cannot move left and i am at row 0, so I gotta go outta bounds
            if row == 0 and self.bay[row][columns].name != '   ':
                row = row - 1
                moves = moves + 1
                col = columns
                moves = moves + 1 
            # I can move left   
            elif row == 0 and self.bay[row][columns].name == '   ':
                col = columns
                moves = moves + 1   
            if col == openColumn:
                break

        # Have moved to where we want to be,
        # now we check whether or not we can go down
        if row == -1:
            # Row is equal to 0 now
            row = row + 1 
            moves = moves + 1
        
        # Count how many '   ' we have available from our coordinate position
        # to see how many moves we can make down
        SHIPROW = len(self.bay)
        if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1,-1))
                return movesAndCoord

        count = 0
        for x in range(row + 1,SHIPROW):
            if self.bay[x][col].name == '   ':
                count = count + 1
        row = row + count
        moves = moves + count
        
        # I have moved as much down as I can, now I store my moves and coords
        movesAndCoord.append(moves)
        movesAndCoord.append((row,col))
        return movesAndCoord
    
    def load(self, coord: tuple[int, int],
             openColumn: int, minMoves: int) -> tuple[int, int, int]:
        movesAndCoord = []
        moves = 0
        MaxMoves = minMoves
        SHIPCOL = len(self.bay[0])
        SHIPROW = len(self.bay)
        row, col = coord # Row = -1, col = -1 here
        #row, col = (-1, -1)

        # Goes from 0, 1, 2, 3 ... , 11
        for columns in range(0, SHIPCOL): 
            moves = moves + 1
            col = columns
            if columns == openColumn:
                break
        
        # We are now at our desired column,
        # now we have to see how far down we can go down
        # Row is still -1, but our col is now in bounds
        count = 0
        for x in range(0,SHIPROW): #range of [0,8)
            if self.bay[x][col].name == '   ':
                count = count + 1
            else: 
                break

        #print("count: ")
        #print(count)

        # Count stores the amount of moves we have to go down
        row = row + count
        #print(row)
        moves = moves + count

        # I have moved as much down as I can, now I store my moves and coords
        movesAndCoord.append(moves)
        movesAndCoord.append((row,col))

        return movesAndCoord
    
    def move_right(self, coord: tuple[int, int],
                   openColumn: int, minMoves: int) -> tuple[int, int, int]:
        movesAndCoord = []
        moves = 0
        MaxMoves = minMoves
        SHIPCOL = len(self.bay[0])
        row, col = coord

        # Flag is true when we are at col == open Column
        # and we have something to sit on
        # Goes from column col 9,10,11
        for columns in range(col+1,SHIPCOL): 
            # I am able to move to the right
            if self.bay[row][columns].name == '   ': 
                # Set our curr col to be the backwards iterations
                col = columns
                moves = moves + 1
            # Im in the outta bounds region right now,
            elif row == -1 and col != openColumn:
                col = columns
                moves = moves + 1
                # I cant move right so i move up 
            elif self.bay[row][columns].name != '   ': 
                # While i cant go left and I can still keep moving up
                while row != 0: 
                    row = row - 1
                    moves = moves + 1
                    # Means that I can move right without going outta bounds
                    if row != 0 and self.bay[row][columns].name == '   ': 
                        col = columns
                        moves = moves + 1
                        break

            if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1,-1))
                return movesAndCoord
            # I cannot move right and i am at row 0, so I gotta go outta bounds
            if row == 0 and self.bay[row][columns].name != '   ': 
                row = row - 1
                moves = moves + 1
                col = columns
                moves = moves + 1    
            # I can move right
            elif row == 0 and self.bay[row][columns].name == '   ': 
                col = columns
                moves = moves + 1
            if col == openColumn:
                break

        # Have moved to where we want to be,
        # now we check whether or not we can go down
        if row == -1:
            row = row + 1 #row is equal to 0 now
            moves = moves + 1
        
        # Count how many '   ' we have available from our coordinate position
        # to see how many moves we can make down
        
        SHIPROW = len(self.bay)

        if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1,-1))
                return movesAndCoord

        count = 0
        for x in range(row + 1,SHIPROW):
            if self.bay[x][col].name == '   ':
                count = count + 1

        row = row + count
        moves = moves + count
            
        # I have moved as much down as I can, now I store my moves and coords
        movesAndCoord.append(moves)
        movesAndCoord.append((row,col))

        return movesAndCoord
    
    def get_stacked(self, coords: tuple[int, int]) -> int:
        row , col = coords
        count = 0

        for x in reversed(range(row)):
            if self.bay[x][col].name != '   ':
                count = count + 1
            else:
                continue
        return count