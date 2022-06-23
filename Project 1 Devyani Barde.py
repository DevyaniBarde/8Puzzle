
"""
Created on Wed Mar 10 21:53:45 2021

@author: Shimpli Kalse
@author: Devyani Barde
"""
import numpy as np
import time
from copy import deepcopy

# Taking input from user as an initial state and handling error for invalid input

def inputo(): 
    global initial_state
    initial_state = []
    print(" Input values from range 0-8 for desired goal state(0 is the blank tile)")
    for i in range(0,9):
        x = int(input("Enter values for tiles :"))
        initial_state.append(x)
    for ele in initial_state:
        if ele < 0 or ele > 8:
            print("Invalid Input")
            inputo()
 
# Taking input from user as desired goal state and handling error for invalid input

def goalo():
    global goal
    goal = []
    print(" Input values from range 0-8 for desired goal state(0 is the blank tile)")
    for i in range(0,9):
        x = int(input("Enter values for tiles :"))
        goal.append(x)
    for ele in goal:
        if ele < 0 or ele > 8:
            print("Invalid Input")
            goalo()


# function to take the input of initial states and analysing the best path to goal state
def best_path(state):
    bestsolution = np.array([], int).reshape(-1, 9)
    count = len(state) - 1
    while count != -1:
        bestsolution = np.insert(bestsolution, 0, state[count]['initial_state'], 0)
        count = (state[count]['parent_node'])
    return bestsolution.reshape(-1, 3, 3)

# function to calculate Manhattan distance cost between inital tile(input) and final goal
def mh_dis(initial_state, goal):
    u = abs(initial_state // 3 - goal // 3)
    v = abs(initial_state % 3 - goal % 3)
    mhcost = u + v
    return sum(mhcost[1:])

# funtion to check the distinctiveness of the iteration(i) state, to check if it was previously traversed
def all(checkarray):
    set=[]
    for i in set:
        for checkarray in i:
            return 1
        else:
            return 0

# fucntion to compute the number of misplaced tiles between the given state and  goal state
def misplaced(initial_state,goal):
    mscost = np.sum(initial_state != goal) - 1
    return mscost if mscost > 0 else 0

# fucntion to determine the coordinates of every state(initial or goal)
def coordinates(initial_state):
    pos = np.array(range(9))
    for w, s in enumerate(initial_state):
        pos[s] = w
    return pos

# code for 8 puzzle evaluation using Manhattan heuristics
def eval(initial_state, goal):
    steps = np.array([('up', [0, 1, 2], -3),('down', [6, 7, 8],  3),('left', [0, 3, 6], -1),('right', [2, 5, 8],  1)],
                dtype =  [('move',  str, 1),('position', list),('head', int)])

    state1 = [('initial_state',  list),('parent_node', int),('gn',  int),('hn',  int)]
    
 # initializing the variables :parent_node, gn and hn where hn is manhattan distance function call 
    costg = coordinates(goal)
    parent_node = -1
    gn = 0
    hn = mh_dis(coordinates(initial_state), costg)
    state = np.array([(initial_state, parent_node, gn, hn)], state1)

# using priority queues where position treated as keys and fn as value.
    priorityq = [('position', int),('fn', int)]
    priority = np.array( [(0, hn)], priorityq)

    while 1:
        priority = np.sort(priority, kind='mergesort', order=['fn', 'position'])     
        position, fn = priority[0]                                                 
        priority = np.delete(priority, 0, 0)  
        # sorting priority queue using merge sort                 
        initial_state, parent_node, gn, hn = state[position]
        initial_state = np.array(initial_state)
        # code to spot the blank square in input 
        blank = int(np.where(initial_state == 0)[0])       
        gn = gn + 1                              
        d = 1
        start_time = time.time()
        for s in steps:
            d = d + 1
            if blank not in s['position']:
                # generate new state as copy of current
                openstates = deepcopy(initial_state)                   
                openstates[blank], openstates[blank + s['head']] = openstates[blank + s['head']], openstates[blank]             
                # The distinct function is called to check previous traversal
                if ~(np.all(list(state['initial_state']) == openstates, 1)).any():    
                    end_time = time.time()
                    if (( end_time - start_time ) > 1):
                        print(" 8 puzzle can not be solved for given set of input  ! \n")
                        exit 
                    # calls the mh_dis function to calcuate the manhattan distance 
                    hn = mh_dis(coordinates(openstates), costg)    
                     # generate and add new state in the list                    
                    q = np.array([(openstates, position, gn, hn)], state1)         
                    state = np.append(state, q, 0)
                    # f(n): additon of the cost to reach the node plus cost to reach goal from current node 
                    fn = gn + hn                                        
            
                    q = np.array([(len(state) - 1, fn)], priorityq)    
                    priority = np.append(priority, q, 0)
                      # Checking if the node in openstates are matching the goal state given by user.  
                    if np.array_equal(openstates, goal):                              
                        print('  8 puzzle can be solved for given set of input ! \n')
                        return state, len(priority)
        
                        
    return state, len(priority)


# code for 8 puzzle evaluation using misplaced tiles in initial_state
def eval_misplaced(initial_state, goal):
    steps = np.array([('up', [0, 1, 2], -3),('down', [6, 7, 8],  3),('left', [0, 3, 6], -1),('right', [2, 5, 8],  1)],
                dtype =  [('move',  str, 1),('position', list),('head', int)])

    state1 = [('initial_state',  list),('parent_node', int),('gn',  int),('hn',  int)]

    costg = coordinates(goal)
    # initializing the parent node, gn and hn, where hn is misplaced function call  
    parent_node = -1
    gn = 0
    hn = misplaced(coordinates(initial_state), costg)
    state = np.array([(initial_state, parent_node, gn, hn)], state1)

   #using priority queue where position treated as keys and fn as value.
    priorityq = [('position', int),('fn', int)]

    priority = np.array([(0, hn)], priorityq)
    
    while 1:
        priority = np.sort(priority, kind='mergesort', order=['fn', 'position'])      
        position, fn = priority[0]       
        # sort priority queue using merge sort,the first element is picked for exploring.                                          
        priority = np.delete(priority, 0, 0)                         
        initial_state, parent_node, gn, hn = state[position]
        initial_state = np.array(initial_state)
         # Identify the blank square in input 
        blank = int(np.where(initial_state == 0)[0])   
        # Increase cost g(n) by 1  
        gn = gn + 1                             
        c = 1
        start_time = time.time()
        for s in steps:
            c = c + 1
            if blank not in s['position']:
                 # generate new state as copy of current
                openstates = deepcopy(initial_state)         
                openstates[blank], openstates[blank + s['head']] = openstates[blank + s['head']], openstates[blank]
                # The check function is called, if the node has been previously explored or not. 
                if ~(np.all(list(state['initial_state']) == openstates, 1)).any():          
                    end_time = time.time()
                    if (( end_time - start_time ) > 1):
                        print(" 8 puzzle can NOT be solved for given set of input ! \n")
                        break
                    # calls the Misplaced function to compute the cost 
                    hn = misplaced(coordinates(openstates), costg) 
                    # generate and add new state in the list                    
                    q = np.array([(openstates, position, gn, hn)], state1)         
                    state = np.append(state, q, 0)
                    # f(n) is the sum of cost to reach node and the cost to reach fromt he node to the goal state
                    fn = gn + hn                                        
                    q = np.array([(len(state) - 1, fn)], priorityq)
                    priority = np.append(priority, q, 0)
                    # Checking if the node in openstates are matching the goal state.
                    if np.array_equal(openstates, goal):                      
                        print('8 puzzle can be solved for given set of input ! \n')
                        return state, len(priority)
                        
    return state, len(priority)



# ----------Taking inputs and calling defined functions as per choice provided -----------------


 

# function call to ask for input
inputo()      
goalo()


n = int(input("1. Manhattan distance \n2. Misplaced tiles \n"))
if(n!=1 and n!=2):
# handling wrong input from user
   print('please choose correct input, either 1 or 2')   
   n = int(input("1. Manhattan distance \n2. Misplaced tiles \n"))  


if(n ==1 ): 
    state, visited = eval(initial_state, goal) 
    bestpath = best_path(state)
    print(str(bestpath).replace('[', ' ').replace(']', ''))
    tot_steps = len(bestpath) - 1
    print('Steps to reach goal:',tot_steps)
    expanded = len(state) - visited
    print('Total nodes expanded: ',expanded, "\n")
    print('Total generated:', len(state))

if(n == 2):
    state, visited = eval_misplaced(initial_state, goal) 
    bestpath = best_path(state)
    print(str(bestpath).replace('[', ' ').replace(']', ''))
    tot_steps = len(bestpath) - 1
    print('Steps to reach goal:',tot_steps)
    expanded = len(state) - visited
    print('Total nodes expanded: ',expanded, "\n")
    print('Total generated:', len(state))  


    
