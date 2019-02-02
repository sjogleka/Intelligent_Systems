from queue import PriorityQueue

## Main Class Solver
class Solver:
    heuristic=None
    f=None
    num_of_instances=0
    def __init__(self,state,parent,action,g,hueristic_type):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.g = parent.g + g
        else:
            self.g = g
        if hueristic_type == 0:#Select manhattan as heuristic if heuristic type is given by user is 0
            self.hueristic_type=0
            self.manhatten_heuristic()
            self.f=self.heuristic+self.g
        else:
            self.hueristic_type = 1#Select manhattan as heuristic if heuristic type is given by user is 1
            self.misplaced_heuristic()
            self.f = self.heuristic + self.g
        Solver.num_of_instances+=1

    ### Manhatten heuristic Calculation
    def manhatten_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    ### Misplaced heuristic Calculation
    def misplaced_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            self.heuristic=self.heuristic+i

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    ## Method to find valid actions: U:- up, D:- Down, L:= Left, R:- Right
    @staticmethod
    def find_valid_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action
## Generate successors based on valid actions
    def generate_successor(self):
        successors=[]
        generated_nodes = 0
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_valid_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action is 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action is 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action is 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            successors.append(Solver(new_state,self,action,1,self.hueristic_type))
        return successors
    ## find solution in reverse order
    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        print('Depth of the solution is : ', len(solution))
        return solution

 # A function to show data in Solver format
def convert(state):
    for i in state:
        print(str(i[0:3])+'\n'+str(i[3:6])+'\n'+str(i[6:9]))
        print('------------')
    return

def Astar_search(initial_state,hueristic_type):
    count=0
    explored=[]#Array to store explored nodes
    start_node=Solver(initial_state,None,None,0,hueristic_type)
    q = PriorityQueue()#Creating object of PriorityQueue
    q.put((start_node.f,count,start_node))#Enqueueing the elements in priority queue

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.goal_test(): #Checking if current goal state matches with Goal State provided by user
            print('Explored Nodes :')
            convert(explored) #Converting explored(Goal States and printing them)
            print('Goal!')
            print('Number of Nodes Expanded:', len(explored))#Here no. of explored nodes will be equal to no. of elements present in explored array.
            return node.find_solution()

        successors=node.generate_successor()#Generates child of current node
        for child in successors:
            if child.state not in explored:#Check if child is present in explored  or not if not then go inside if condition
                count += 1
                q.put((child.f,count,child))#Inserting generated child node into queue
    return

#################################################################################################################
########################################### Input Block ####################$$###################################
#################################################################################################################
state=[]
print("****************************** 8 Puzzle Solver using A* algorithm ****************************** ")
print("Please insert input in below order :-\n0 1 3 4 2 5 7 8 6")
print("Enter Now :")
arr = input().split()
for i in range(0,9):
    arr[i]=int(arr[i])
#print(arr)
state.append(arr)#Storing Input array from gettign from user
print("You have entered :- \n")
convert(state)#Converting Input State into 3x3 format
print("Please insert goal in below order :-\n1 2 3 4 5 6 7 8 0")
print("Enter Now :")
goal = input().split()
for i in range(0,9):
    goal[i]=int(goal[i])
#print(arr)
goalconvert=[]
goalconvert.append(goal)#Storing Goal state given by user
print("You have entered :- ")
convert(goalconvert)#Converting Goal State into 3x3 format
print("Enter the type of heuristic :\n0. Manhattan,\n1. Misplaced")
hueristic_type = int(input())
################################################################################################################
################################################################################################################
Solver.num_of_instances = 0
Solver.goal_state=goal
astar = Astar_search(state[0],hueristic_type)#Passing the aray and the heuristic to A star function
#print('A*:',astar)
print('No of Nodes Generated:', Solver.num_of_instances)
print()
print('------------------------------------------')