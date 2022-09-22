from email import iterators
from operator import length_hint
from time import time
from SearchAgent import SearchAgent
from Node import Node
from browser import document, window
import javascript


def draw_weights():
    ctx.font = "18px Arial"
    visited = []
    for node1 in agent.graph.keys():
        for node2 in agent.graph[node1].children.keys():
            """if (node1,node2) in visited or (node2, node1) in visited:
                continue
            visited.append((node1,node2))"""
            x1, y1 = agent.graph[node1].position
            x2, y2 = agent.graph[node2].position
            weight = agent.graph[node1].children[node2]
            ctx.fillText(weight,(x1+x2)/2, (y1+y2)/2)

old = []
def animate_graph():
    global yield_result, val, any_change, agent, old, node_type
    print("Inside 'animate_graph' : ", val)

    #if len(val) <= len(old):
    """or i in range(len(val)):
            if old[i] != val[i]:
                val = val[2:]
                queue = old[-1:i-2:-1]
        start = queue[0]
        for node in queue[1:]:"""
    any_change = True
    delete_and_draw()
        



    start = val[0]
    for node in val[1:]:
        end = node
        print("start : ",start,"End : ",end)
        ctx.lineWidth = 6
        ctx.beginPath()
        ctx.strokeStyle = 'red'
        x1,y1 = agent.graph[start].position
        ctx.moveTo(x1,y1)

        x2,y2 = agent.graph[end].position
        ctx.lineTo(x2,y2)

        ctx.stroke()
        ctx.lineWidth = 1
        start = end
        ctx.strokeStyle = 'black'
        for circle_node in agent.graph.keys():
            if agent.start == circle_node:
                node_type = 'start'
            elif agent.goal == circle_node:
                node_type = 'goal'
            else:
                node_type = 'normal'
            circle(*agent.graph[circle_node].position, circle_node)
        draw_weights()
        #if end == agent.goal:
    ctx.strokeStyle = 'black'
    old = val


def circle(x,y, node):
    global node_type, colors_to_fill_inside
    ctx.beginPath()
    ctx.arc(x,y, radius, 0, 2 * javascript.Math.PI) #start angle, end angle
    ctx.fillStyle = colors_to_fill_inside[node_type]
    ctx.StrokeStyle = 'black'
    ctx.fill()
    ctx.stroke()
    node_type = 'normal'
    # Drawing node name
    ctx.fillStyle = 'black'
    ctx.font = "20px Arial"
    ctx.textBaseline = "middle"
    ctx.fillText(node, x, y - 5)
    #ctx.fillText(node, x1 - 6, y1)

    # Drawing Heuristics
    ctx.font = "13px Arial"
    ctx.fillText(agent.graph[node].heuristics,  x, y + 14)
    

def delete_and_draw():
    # goal node  is used for setting goal node color
    global any_change, goal_node, node_type, agent
    if any_change:
        print("Delete")

        ctx.clearRect(0, 0, document['canvas'].offsetWidth, document['canvas'].offsetHeight)
        
        visited = []
        #for node in agent.graph.values():
        for node in agent.graph.keys():
            if (node == agent.goal):
                node_type = 'goal'
            elif (node == agent.start):
                node_type = 'start'
            else:
                node_type = 'normal'
            
            x1,y1 = agent.graph[node].position

            children = agent.graph[node].children
            for child_node ,weight in children.items():
                if (node, child_node) in visited or (child_node, node) in visited:
                    continue
                visited.append((node,child_node))
                ctx.beginPath()
                ctx.StrokeStyle = 'black'
                ctx.moveTo(x1,y1)

                x2,y2 = agent.graph[child_node].position
                ctx.lineTo(x2,y2)
                
                ctx.font = "18px Arial"
                ctx.fillText(weight,(x1+x2)/2, (y1+y2)/2)

                ctx.stroke()
            
            circle(*agent.graph[node].position, node)
            """# Drawing node name
            ctx.fillStyle = 'black'
            ctx.font = "20px Arial"
            ctx.textBaseline = "middle"
            ctx.fillText(node, x1, y1 - 5)
            #ctx.fillText(node, x1 - 6, y1)

            # Drawing Heuristics
            ctx.font = "13px Arial"
            ctx.fillText(agent.graph[node].heuristics,  x1, y1 + 14)"""
        
        any_change = False
        
    if agent.status == 'searching':
        window.setTimeout(agent_search, 24)

        
def solve(algo):
    global agent, yield_result, any_change
    agent.status = 'searching'
    yield_result = map_algorithm[algo]()
    #print(next(yield_result))
    ####any_change = True
    delete_and_draw()
    #for x in yield_result:
        #timeout_var = window.setTimeout(animate_graph, 800)
        #print(x)

    """ if selected_algorithm in map_algorithm:
        try:
            print(next(yield_result))
        except Exception as e:
            print("Exception")"""
    
def next_iteration():
    global yield_result, val
    #print("ok inside 'next_iteration'")
    val = next(yield_result)

def agent_search():
    global any_change, start_time
    #print("ok inside 'agent_search'")
    if agent.status == 'searching':
        
        try:
            now_time = javascript.Date.now()
            #print("ok inside")
            #print(now_time, start_time)
            if now_time - start_time >= 800:
                window.setTimeout(animate_graph, 1)
                next_iteration()
                start_time = now_time
            ####any_change = True
            delete_and_draw()
        except Exception as e:
            print("Exception")
            agent.status = 'idle'
            

    


def graph_setup(event):
    global counter, node_name, tool, agent, node_selected, start_node, end_node, radius, any_change, selected_node_\
        ,goal_node, start_time

    x = event.x - 240
    y = event.y - 26

    
    def find_edge_ends(radius):
        visited = []
        for node in agent.graph.values():
            children = node.children
            x1,y1 = node.position
            for child_node in children.keys():
                
                if (node, child_node) in visited or (child_node, node) in visited:
                    continue
                visited.append((node,child_node))
                x2,y2 = agent.graph[child_node].position
                mid_x, mid_y = (x1 + x2)/2, (y1 + y2)/2
                if x <= mid_x + radius and x >= mid_x - radius and \
                    y <= mid_y + radius and y >= mid_y - radius:
                    
                    return node.name ,child_node
        return -1,-1

    def find_node():
        for node in agent.graph.values():
            if x <= node.position[0] + radius and x >= node.position[0] - radius and \
                    y <= node.position[1] + radius and y >= node.position[1] - radius:
                return node.name
        return -1

    

    #print(tool)
    #print(x,y)

    
    if tool == 'nodeAdd':
        
        ctx.textAlign = "center"

        # Drawing node name
        ctx.fillStyle = 'black'
        ctx.font = "20px Arial"
        ctx.textBaseline = "middle"
        node_name = chr(counter%26 + 65)
        ctx.fillText(node_name, x, y - 5)

        # Creating actual node in graph
        agent.graph[node_name] = Node(node_name, position = (x, y))

        # Drawing Heuristics        
        ctx.font = "13px Arial"
        ctx.fillText("1",  x, y + 14)

        #circle(*agent.graph[node_name].position, node_name)
        any_change = True
        delete_and_draw()
        counter += 1
    
    elif tool == 'nodeDelete':
        start_node = find_node()
        if start_node == -1:
            return
        
        # setting goal and agent to none, if the node is deleted . Not needed per ses
        if agent.goal == start_node:
            agent.goal = None
        elif agent.start == start_node:
            agent.start = None

        child_nodes = agent.graph[start_node].children.keys()
        
        del agent.graph[start_node]

        for child in child_nodes:
            del agent.graph[child].children[start_node]
        any_change = True
        delete_and_draw()



    elif tool == 'edgeAdd' :
        edge_node = find_node()
        if edge_node == -1:
            return
        elif not node_selected:
            #print(edge_node)
            node_selected = True
            start_node = edge_node
            selected_node_ = start_node
            any_change = True
            #delete_and_draw()
            return

        elif node_selected:
            #print(edge_node)
            end_node = edge_node
            if start_node == end_node:
                node_selected = False
                return

            # to avoid edge drawing redundantly
            if end_node in agent.graph[start_node].children.keys() or start_node in agent.graph[end_node].children.keys():
                node_selected = False
                return
            x1,y1 = agent.graph[start_node].position
            x2,y2 = agent.graph[end_node].position
            
            ctx.beginPath()
            ctx.moveTo(x1,y1)
            ctx.lineTo(x2,y2)
            ctx.stroke()

            ctx.fillStyle = 'black'
            ctx.font = "18px Arial"
            ctx.fillText(1,(x1+x2)/2, (y1+y2)/2)

            agent.graph[start_node].children.update({end_node: 1})
            agent.graph[end_node].children.update({start_node: 1})

            #print(agent.graph[start_node].children)
            any_change = True
            delete_and_draw()
            node_selected = False


    elif tool == 'edgeDelete':
        edge_node = find_node()
        if edge_node == -1:
            return
        elif not node_selected:
            print("start : ",edge_node)
            node_selected = True
            start_node = edge_node
            return

        elif node_selected:
            end_node = edge_node
            print("end : ", end_node)
            if start_node == end_node:
                node_selected = False
                return

            if end_node in agent.graph[start_node].children.keys():
                del agent.graph[start_node].children[end_node]
                del agent.graph[end_node].children[start_node]

                any_change = True
                delete_and_draw()
            node_selected = False

    elif tool == 'heuristics':
        node_name = find_node()
        if node_name == -1:
            return
        DialogBoxVisibility(True)
       
    
    elif tool == 'weights':
        start_node, end_node = find_edge_ends(radius)
        if (start_node == -1):
            return

        #print(node,child_node)
        DialogBoxVisibility(True)
    
    elif tool == 'setgoal':
        # incase -1 is returned old goal node is kept track of
        old_goal = agent.goal
        agent.goal = find_node()
        #print('goal_set', goal_node)
        if agent.goal == -1 or agent.goal == agent.start:
            agent.goal = old_goal
            return
        #agent.goal = goal_node
        any_change = True
        delete_and_draw()

    elif tool == 'setstart':
        # incase -1 is returned old start node is kept track of
        old_start = agent.start
        agent.start = find_node()
        if agent.start == -1 or agent.goal == agent.start:
            agent.start = old_start
            return
        any_change = True
        delete_and_draw()
        
  
def DialogBoxVisibility(value):
    global any_change
    if value:
        document["weights-modal"].showModal()
    else:
        document["weights-modal"].close()
        delete_and_draw()
        #any_change = False


#
def weightsUpdate():
    global any_change
    validated = document["weights-form"].reportValidity()
    if validated:
        result = document["weights-input"].value
        agent.graph[start_node].children.update({end_node: result})
        agent.graph[end_node].children.update({start_node: result})
        any_change = True
        #delete_and_draw() . why not working
        

    
def heuristicsUpdate():
    global any_change
    validated = document["weights-form"].reportValidity()
    if validated:
        result = document["weights-input"].value
        agent.graph[node_name].heuristics = result
        any_change = True

def tool_select(do):
    global tool
    tool = do

def algo_select(algo):
    #print(algo)
    global selected_algorithm
    selected_algorithm = algo





canvas = document["canvas"]
ctx = canvas.getContext("2d")
window_width = window.innerWidth
window_height = window.innerHeight
#canvas["width"] = window_width - 190
canvas["height"] = window_height - 130
canvas["width"] = window_width - 330

"""print(document['canvas'].offsetWidth)
print(document['canvas'].offsetHeight)"""

# type = goal, normal, start
node_type = 'normal' 
goal_node = None
colors_to_fill_inside = {'goal' : "green", 'normal' : 'white', 'start': 'orange'}
colors_to_fill_text = {'goal' : 'white', 'normal' : 'black', 'start':'black'}
colors_for_border = {True : 'red', False : 'black'}

tool = None
selected_algorithm = None

counter = 0
node_name = chr(counter + 65)
radius = 20

# On clicking , if any node is selected
node_selected = False

# selected node
selected_node_ = None

# for edge formation
start_node = None
end_node = None

# keeping track of change
any_change = False

# iterator, timeout variable to stop window execution
yield_result = None
val = None


agent = SearchAgent()
map_algorithm = {'bfs' : agent.bfs, 'dfs' : agent.dfs \
    ,'bs' : agent.bs, 'bb' : agent.bb, 'bb-h' : agent.bb_h, 'astar' : agent.a_star }



document['nodeAdd'].bind('click', lambda e: tool_select('nodeAdd'))
document['nodeDelete'].bind('click', lambda e: tool_select('nodeDelete'))
document['edgeAdd'].bind('click', lambda e: tool_select('edgeAdd'))
document['edgeDelete'].bind('click', lambda e: tool_select('edgeDelete'))
document['heuristics'].bind('click', lambda e: tool_select('heuristics'))
document['weights'].bind('click', lambda e: tool_select('weights'))

# Weights and heuristics
document["weights-close"].bind("click", lambda e: DialogBoxVisibility(False))
document["weights-update"].bind("click", lambda e:  weightsUpdate() if tool == 'weights' else heuristicsUpdate())

# setting goal and start
document['setgoal'].bind('click', lambda e: tool_select('setgoal'))
document['setstart'].bind('click', lambda e: tool_select('setstart'))

document['dfs'].bind('click', lambda e: algo_select('dfs'))
document['bfs'].bind('click', lambda e: algo_select('bfs'))
document['hc'].bind('click', lambda e: algo_select('hc'))
document['bs'].bind('click', lambda e: algo_select('bs'))
document['bb'].bind('click', lambda e: algo_select('bb'))
document['bb-h'].bind('click', lambda e: algo_select('bb-h'))
document['astar'].bind('click', lambda e: algo_select('astar'))

document['solve'].bind('click', lambda e: solve(selected_algorithm))

document['canvas'].bind('mousedown', lambda e: graph_setup(e))

"""def request_again():
    window.requestAnimationFrame(graph_setup)

window.setTimeout(request_again, 24)"""
start_time = javascript.Date.now()
