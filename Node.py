
class Node:
    def __init__(self, name, position, cost=0, heuristics=1):
        self.name = name
        self.position = position
        #self.cost = cost
        self.heuristics = heuristics
        self.children = dict()
    