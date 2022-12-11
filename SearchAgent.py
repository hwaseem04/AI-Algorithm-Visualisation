

class SearchAgent:

    def __init__(self, graph=dict(), start=None, goal=None, status='idle'):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.status = status
        self.queue = []
        self.no_enqueue = 0

    def dfs(self):
        if self.goal == None or self.start == None or len(self.graph) < 2:
            return

        self.no_enqueue = 0
        Final_result = []
        self.queue = [[self.start]]
        flag = 0
        while(len(self.queue) != 0):
            current_path = self.queue.pop(0)
            current_node = current_path[-1]
            if current_node == self.goal:
                flag = 1
                break

            for child_node in self.graph[current_node].children.keys():
                if child_node not in current_path:
                    self.queue.append(current_path + [child_node])
                    self.no_enqueue += 1
            
            self.queue = sorted(self.queue)
            if (len(self.queue) != 0):
                Final_result.append(self.queue[0])
        if (flag == 0):
            return None
        print(Final_result)
        return Final_result
        


    def bfs(self):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return
        self.no_enqueue = 0
        Final_result = []
        self.queue = [[self.start]]
        flag = 0
        goalpath = []
        while(len(self.queue) != 0):
            length = len(self.queue)
            new_extension = []
            for k in range(length):
                current_path = self.queue[k]
                current_node = current_path[-1]
                for child in self.graph[current_node].children.keys() :
                    if child not in current_path:
                        temp = current_path + [child]
                        new_extension.append(temp)
                        self.queue.append(temp)
                        self.no_enqueue += 1
                        if(child == self.goal):
                            flag = 1
                            goalpath = temp
                            print(temp)
                            break
            
            new_extension = sorted(new_extension)
            Final_result.extend(new_extension)
            if (flag == 1):
                break

            self.queue = self.queue[length:]
            self.queue = sorted(self.queue)
        if (flag == 0):
            return None
        index = Final_result.index(goalpath)
        Final_result = Final_result[:index+1]
        print(Final_result)
        return Final_result

    def hc(self):
        if self.goal == None or len(self.graph) < 2:
            return
        self.no_enqueue = 0
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
                self.no_enqueue += 1
                element[0] = int(self.graph[child_node].heuristics)
                #print(element)
                sub_list.append(element)
                #self.priority_queue(element)
                if self.goal in element:
                    self.no_enqueue += 1
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
        self.no_enqueue = 0
        B = 3
        Final_result = []
        self.queue = []

        for child_node in self.graph[self.start].children.keys():
            element = [int(self.graph[child_node].heuristics), self.start, child_node]
            #print(element)
            self.priority_queue(element)
            self.no_enqueue += 1
            if self.goal in element:
                self.no_enqueue += 1
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
                    self.no_enqueue += 1
                    element[0] = int(self.graph[child_node].heuristics)
                    #print(element)
                    self.priority_queue(element)
                    
                    if self.goal in element:
                        Final_result.append([element])
                        self.no_enqueue += 1
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
        self.no_enqueue = 0
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
                self.no_enqueue += 1
                sub_list.append(element)
                
                if self.goal in element:
                    Final_result.append([element])
                    self.no_enqueue += 1
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
        self.no_enqueue = 0
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
                self.no_enqueue += 1
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
                    self.no_enqueue += 1
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
        self.no_enqueue = 0
        # Extended list
        visited = {key : 0 for key in self.graph}
        self.queue = [[0, self.start]]
        Final_result = []
        while len(self.queue) != 0:
            sub_list = []
            #temp = self.queue[0]
            choosen_node = self.queue[0][-1]
            for child_node in self.graph[choosen_node].children.keys():
                if child_node in self.queue[0]:
                    continue
                if visited[child_node] == 1:
                    continue
                else:
                    visited[child_node] = 1
                element = self.queue[0] + [child_node]
                self.no_enqueue += 1
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
                    self.no_enqueue += 1
                    print("GOAL")
                    return Final_result
                
            self.queue.pop(0)
            if len(sub_list) == 0:
                continue
            sub_list = sorted(sub_list)
            for elem in sub_list:
                self.priority_queue(elem)
            
            Final_result.append(sub_list)
            print(sub_list)
            print(self.queue)
            print("-------------")
        
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
