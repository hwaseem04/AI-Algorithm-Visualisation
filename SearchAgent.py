class SearchAgent:
    def __init__(self, graph=dict(), start=None, goal=None, status='idle'):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.status = status
        self.no_enqueue = 0 
        self.dfs_cnt = "start"
        self.hc_cnt = "start"
    def Key(self,x):
            return self.graph[x].heuristics   
    def max(self,x):
        return x[0]
    def bfs(self):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return None
        temp_path = [[self.start]]
        loop = 'keep_going'
        self.no_enqueue = 0  
        for i in temp_path: # Making use of Queue implementation of BFS
            for j in list(self.graph[i[-1]].children.keys()) :
                if(j not in i):
                    x = i.copy()
                    x.append(j)
                    temp_path.append(x)
                    self.no_enqueue+=1
                    if(j==self.goal):
                        temp_path = temp_path[1:]
                        loop = 'end'
                        break
            if(loop=='end'):
                break
        print(temp_path)
        return temp_path
    def dfs(self,path=[],st=0):
        # Implemented DFS using recursive Call
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return None
        
        elif(self.dfs_cnt=="end"):
            print(path[1:])
            return path[1:]
    
        else: 
            if(st==0):
                self.no_enqueue = 0  
                path.append([self.start])

            node_vis = path[-1][-1]
            Copy = path[-1].copy()

            for i in list(self.graph[node_vis].children.keys()):
                if i not in Copy:
                    
                    Copy.append(i)
                    path.append(Copy.copy())
                    self.no_enqueue +=1

                    if(i==self.goal):
                        self.dfs_cnt='end'
                    else:
                        pass
                    x = self.dfs(path=path,st=1)

                    if(self.dfs_cnt=='end'):
                        return x
                    else:
                       _ =  Copy.pop()
            return None
    def hc(self,path=[],st=0):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return None
        
        elif(self.hc_cnt=="end"):
            print(path[1:])
            return path[1:]
    
        else: 
            if(st==0):
                self.no_enqueue = 0  
                path.append([self.start])

            node_vis = path[-1][-1]
            Copy = path[-1].copy()

            A = sorted(list(self.graph[node_vis].children.keys()),key = self.Key)

            for i in A  :
                if i not in Copy:
                    Copy.append(i)
                    path.append(Copy.copy())
                    self.no_enqueue +=1

                    if(i==self.goal):
                        self.hc_cnt='end'
                    else:
                        pass
                    x = self.hc(path=path,st=1)

                    if(self.hc_cnt=='end'):
                        return x
                    else:
                       _ =  Copy.pop()
            return None
    def bs(self,w=2):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return None
        temp_path = [[self.start]]
        self.no_enqueue=0
        loop = 'keep_going'
        for i in temp_path: 
            A = sorted(list(self.graph[i[-1]].children.keys()),key=self.Key)[:w]
            for j in A :
                if(j not in i):
                    x = i.copy()
                    x.append(j)
                    temp_path.append(x)
                    self.no_enqueue+=1
                    if(j==self.goal):
                        temp_path = temp_path[1:]
                        loop = 'end'
                        break
            if(loop=='end'):
                break
        print(temp_path)
        return temp_path
    def best(self):
        pass
    def bb(self,h=0,ex=0):
        if self.goal == None or self.start == None or len(self.graph) < 2: ## Create a dialog box to notify user
            return None
        else:
            loop='start'
            path=[[0,self.start]]
            st = 0 
            self.no_enqueue = 0  
            while(loop!='end'):
                Cost=[]
                vis=[]
                for i in path:
                    A = self.graph[i[-1]].children
                    for j in list(A.keys()):
                        if j not in i and not(ex* (j in vis)):
                            Copy=i.copy()
                            Copy[0] = Copy[0] + A[j] + (h* self.graph[j].heuristics)
                            Copy.append(j)
                            if(Copy not in path):
                                Cost.append(Copy)
                if(st==len(self.graph[self.start].children.keys())):
                    path=path[1:]
                    st = len(self.graph[self.start].children.keys())+1
                elif (st<len(self.graph[self.start].children.keys())):
                    st+=1
                Cost.sort(key = self.max)
                path.append(Cost[0])
                if(path[-1][-1]==self.goal):
                    loop='end'
                else:
                    vis.append(path[-1][-1])
                self.no_enqueue +=1
            print(path)
            return [i[1:] for i in path]
    def bb_h(self): # estimated justification
        return self.bb(h=1);
    def bb_ex(self):
        return self.bb(ex=1)
    def a_star(self):
        return self.bb(h=1,ex=1)
    
    def MinMax():
        pass