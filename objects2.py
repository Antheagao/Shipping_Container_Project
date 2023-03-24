class Container:
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight


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

    def get_uniq_coordinates(self, container: str, coord: tuple[int,int]) -> set:
        ROW = len(self.bay)
        COL = len(self.bay[0])
        
        for row in range(ROW):
            for col in range(COL):
                if self.bay[row][col].name == container and (row,col) not in coord:
                    x,y = (row,col)
                    coord.append((x,y))

        return coord

    def get_open_columns(self, coord: list[int]) -> list[int]:
        ROW = len(self.bay)
        COL = len(self.bay[0])
        open = []
        
        for row in range(ROW):
            for col in range(COL):
                if self.bay[row][col].name == '   ' and (col) not in open:
                    x,y = (row,col)
                    if y not in coord:
                        open.append(y)

        return open

    def move_left(self, coord: tuple[int,int], openColumn: int, minMoves: int) -> tuple[int,int,int]:
        movesAndCoord = []
        moves = 0
        MaxMoves = minMoves

        row,col = coord

        #flag is true when we are at col == open Column and we have something to sit on
        for columns in reversed(range(col)): #goes from column 8 to 0
            if self.bay[row][columns].name == '   ': #i am able to move to the left
                col = columns#set our curr col to be the backwards iterations
                moves = moves + 1

            elif row == -1 and col != openColumn:#im in the outta bounds region right now,
                col = columns
                moves = moves + 1
            elif self.bay[row][columns].name != '   ': #i cant move left so i move up 
                while row != 0: #while i cant go left and I can still keep moving up
                    row = row - 1
                    moves = moves + 1
                    if row != 0 and self.bay[row][columns].name == '   ': #means that I can move left without going outta bounds
                        col = columns
                        moves = moves + 1
                        break

            if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1,-1))
                return movesAndCoord

            if row == 0 and self.bay[row][columns].name != '   ': #i cannot move left and i am at row 0, so I gotta go outta bounds
                row = row - 1
                moves = moves + 1
                col = columns
                moves = moves + 1    

            elif row == 0 and self.bay[row][columns].name == '   ': #i can move left
                col = columns
                moves = moves + 1
                

            if col == openColumn:
                break

            

        #have moved to where we want to be, now we check whether or not we can go down
        if row == -1:
            row = row + 1 #row is equal to 0 now
            moves = moves + 1
        
        #count how many '   ' we have available from our coordinate position to see how many moves we can make down
        
        

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
            

        

        #i have moved as much down as I can, now I store my moves and coords
        movesAndCoord.append(moves)
        movesAndCoord.append((row,col))


        return movesAndCoord

    def move_right(self, coord: tuple[int,int], openColumn: int, minMoves: int) -> tuple[int,int,int]:
        movesAndCoord = []
        moves = 0
        MaxMoves = minMoves

        SHIPCOL = len(self.bay[0])

        row,col = coord

        #flag is true when we are at col == open Column and we have something to sit on
        for columns in range(col+1,SHIPCOL): #goes from column col 9,10,11
            if self.bay[row][columns].name == '   ': #i am able to move to the right
                col = columns#set our curr col to be the backwards iterations
                moves = moves + 1

            elif row == -1 and col != openColumn:#im in the outta bounds region right now,
                col = columns
                moves = moves + 1
            elif self.bay[row][columns].name != '   ': #i cant move right so i move up 
                while row != 0: #while i cant go left and I can still keep moving up
                    row = row - 1
                    moves = moves + 1
                    if row != 0 and self.bay[row][columns].name == '   ': #means that I can move right without going outta bounds
                        col = columns
                        moves = moves + 1
                        break

            if moves > MaxMoves:
                movesAndCoord.append(100000)
                movesAndCoord.append((-1,-1))
                return movesAndCoord

            if row == 0 and self.bay[row][columns].name != '   ': #i cannot move right and i am at row 0, so I gotta go outta bounds
                row = row - 1
                moves = moves + 1
                col = columns
                moves = moves + 1    

            elif row == 0 and self.bay[row][columns].name == '   ': #i can move right
                col = columns
                moves = moves + 1
                

            if col == openColumn:
                break

            

        #have moved to where we want to be, now we check whether or not we can go down
        if row == -1:
            row = row + 1 #row is equal to 0 now
            moves = moves + 1
        
        #count how many '   ' we have available from our coordinate position to see how many moves we can make down
        
        

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
            

        

        #i have moved as much down as I can, now I store my moves and coords
        movesAndCoord.append(moves)
        movesAndCoord.append((row,col))


        return movesAndCoord


    def get_stacked(self, coords: tuple[int,int]) -> int:

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