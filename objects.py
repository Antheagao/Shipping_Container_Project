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