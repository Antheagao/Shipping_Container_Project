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

    def move_left(self, curr)


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