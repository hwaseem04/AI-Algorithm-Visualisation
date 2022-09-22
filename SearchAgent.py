
class SearchAgent:

    def __init__(self, graph=dict(), start=None, goal=None, status='idle'):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.status = status

    def dfs(self):
        if self.goal == None or len(self.graph) < 2:
            return
        """print(self.graph)
        print(self.start)
        print(self.goal)"""

        queue = []
        for child_node in self.graph[self.start].children.keys():
            queue.append([self.start, child_node])
        
        queue = sorted(queue)

        while(len(queue) != 0):
            current_node = queue[0][-1]

            if current_node == self.goal:
                print("Final Path : ", queue[0])
                yield queue.pop(0)
                break

            for child_node in self.graph[current_node].children.keys():
                if child_node not in queue[0]:
                    temp = queue[0] + [child_node]
                    queue.insert(1,temp)
            yield queue.pop(0)
            
            queue = sorted(queue)
        self.status = 'idle'


    def bfs(self):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return
        queue = []
        for child in self.graph[self.start].children.keys():
            queue.append([self.start, child])
            
        queue = sorted(queue)
        print(queue)

        for yield_value in queue:
            yield yield_value
            if self.goal in yield_value:
                    self.status = 'idle'
                    return
            
        while(len(queue) != 0):
            length = len(queue)
            for k in range(length):
                current_node = queue[k][-1]
                for child in self.graph[current_node].children.keys() :
                    if child not in queue[k]:
                        temp = queue[k] + [child]
                        queue.append(temp)
                    
            queue = queue[length:]
            queue = sorted(queue)
            print(queue)
            if len(queue) == 0:
                break
            for yield_value in queue:
                yield yield_value
                if self.goal in yield_value:
                    self.status = 'idle'
                    return
            
            for i in queue:
                if self.goal in i:
                    print("GOAL : ", i)
                    self.status = 'idle'
                    return

    def bs(self):
        if self.goal == None or len(self.graph) < 2:
            return
        

    def bb(self):
        if self.goal == None or len(self.graph) < 2:
            return
    def bb_h(self):
        if self.goal == None or len(self.graph) < 2:
            return
    def a_star(self):
        if self.goal == None or len(self.graph) < 2:
            return
        

