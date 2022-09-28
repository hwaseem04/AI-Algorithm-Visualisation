

class SearchAgent:

    def __init__(self, graph=dict(), start=None, goal=None, status='idle'):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.status = status
        self.queue = []

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
    def hc(self):
        if self.goal == None or len(self.graph) < 2:
            return

        Final_result = []
        self.queue = [[int(self.graph[self.start].heuristics), self.start]]

        i = 0
        while len(self.queue) != 0:
            sub_list = []
            temp = self.queue[0]
            choosen_node = self.queue[0][-1]
            for child_node in self.graph[choosen_node].children.keys():
                if child_node in self.queue[0]:
                    continue
                element = self.queue[0] + [child_node]
                element[0] = int(self.graph[child_node].heuristics)
                #print(element)
                sub_list.append(element)
                #self.priority_queue(element)
                if self.goal in element:
                    Final_result.append([element])
                    print("GOAL")
                    return Final_result
            
            sub_list = sorted(sub_list)
            print("SUB LIST" ,sub_list)
            self.queue.remove(temp)

            for elem in sub_list[-1::-1]:
                self.queue.insert(0,elem)
            print("SELF queue ",self.queue)
            Final_result.append([self.queue[0]])

            
            i += 1


    def bs(self):
        if self.goal == None or len(self.graph) < 2:
            return
        # Beam search
        
        B = 3
        Final_result = []
        self.queue = []

        for child_node in self.graph[self.start].children.keys():
            element = [int(self.graph[child_node].heuristics), self.start, child_node]
            #print(element)
            self.priority_queue(element)
            if self.goal in element:
                Final_result.append([element])
                print(Final_result)
                print("GOAL")
                return Final_result

        self.queue = self.queue[:B]
        Final_result.append(self.queue.copy())
        #print(Final_result)
        
        while len(self.queue) != 0:
            temp_queue = self.queue.copy()
            K = len(temp_queue)
            for i in range(K):
                choosen_node = temp_queue[i][-1]
                for child_node in self.graph[choosen_node].children.keys():
                    if child_node in temp_queue[i]:  # To avoid tail biting
                        continue 
                    element = temp_queue[i] + [child_node]
                    element[0] = int(self.graph[child_node].heuristics)
                    #print(element)
                    self.priority_queue(element)
                    
                    if self.goal in element:
                        Final_result.append([element])
                        print(Final_result)
                        print("GOAL")
                        return Final_result

                #print("1",self.queue,"------", temp_queue)
                del self.queue[self.queue.index(temp_queue[i])]
                #print("2",self.queue,"------", temp_queue)
            self.queue = self.queue[:B].copy()
            print(Final_result,"------")
            Final_result.append(self.queue.copy())
            print(Final_result,"------", self.queue)
            # Kind of dead lock case condition below
            if self.queue == []:
                return Final_result

    def bb(self):
        if self.goal == None or len(self.graph) < 2:
            return
        
        self.queue = [[0, self.start]]
        Final_result = []
        while len(self.queue) != 0:
            sub_list = []
            #temp = self.queue[0]
            choosen_node = self.queue[0][-1]
            for child_node in self.graph[choosen_node].children.keys():
                if child_node in self.queue[0]:
                    continue
                element = self.queue[0] + [child_node]
                element[0] += self.graph[choosen_node].children[child_node]
                sub_list.append(element)
                
                if self.goal in element:
                    Final_result.append([element])
                    print("GOAL")
                    return Final_result
                
            self.queue.pop(0)
            sub_list = sorted(sub_list)
            for elem in sub_list:
                self.priority_queue(elem)
            
            Final_result.append(sub_list)
            print(sub_list)
            print(self.queue)
            print("-------------")



        
    def bb_h(self):
        if self.goal == None or len(self.graph) < 2:
            return

        self.queue = [[0, self.start]]
        Final_result = []
        while len(self.queue) != 0:
            sub_list = []
            #temp = self.queue[0]
            choosen_node = self.queue[0][-1]
            for child_node in self.graph[choosen_node].children.keys():
                if child_node in self.queue[0]:
                    continue
                element = self.queue[0] + [child_node]
                # Update weight
                element[0] += self.graph[choosen_node].children[child_node]
                # Update heuristc aptly
                prev_node = element[-2]
                if prev_node != self.start:
                    
                    element[0] += (self.graph[child_node].heuristics - self.graph[prev_node].heuristics)
                    #print(element)
                else:
                    
                    element[0] += (self.graph[child_node].heuristics)
                    #print(element)
                sub_list.append(element)
                
                if self.goal in element:
                    Final_result.append([element])
                    print("GOAL")
                    return Final_result
                
            self.queue.pop(0)
            sub_list = sorted(sub_list)
            for elem in sub_list:
                self.priority_queue(elem)
            
            Final_result.append(sub_list)
            print(sub_list)
            print(self.queue)
            print("-------------")
        

    def a_star(self):
        if self.goal == None or len(self.graph) < 2:
            return

    def priority_queue(self, element):
        
        if len(self.queue) == 0:
            selected_index = None
            self.queue.append(element)
        else:
            selected_index = -1
            for i in range(len(self.queue)):
                if element[0] < self.queue[i][0]:
                    selected_index = i
                    break
                elif element[0] > self.queue[i][0]:
                    selected_index = i + 1
                    continue
                else:
                    if len(element) < len(self.queue[i]):
                        selected_index = i
                    elif len(element) == len(self.queue[i]):
                        if element[-1] < self.queue[i][-1]:
                            selected_index = i
                        else:
                            selected_index = i + 1
                            continue
                    else:
                        selected_index = i + 1
                    break
            self.queue.insert(selected_index, element)
                    
        #print("Inside priority queue :", selected_index, self.queue)
