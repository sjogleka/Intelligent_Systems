from random import randrange
from copy import deepcopy
from random import choice

# A class to create queenstate and identify the best possible children based on number of queens attacking
class QueensState:

    instance_counter = 0
    def __init__(self, queen_positions=None, parent=None,f_cost=0,):

        self.side_length = int(n)

        if queen_positions == None:
            self.queen_num = self.side_length
            self.queen_positions = frozenset(self.random_queen_position())
        else:
            self.queen_positions = frozenset(queen_positions)
            self.queen_num = len(self.queen_positions)

        self.path_cost = 0
        self.f_cost = f_cost
        self.parent = parent
        self.id = QueensState.instance_counter
        QueensState.instance_counter += 1

    # A function to generate queen positions randomly
    def random_queen_position(self):
        ''' Each queen is placed in a random row in a separate column '''
        open_columns = list(range(self.side_length))
        queen_positions = [(open_columns.pop(randrange(len(open_columns))), randrange(self.side_length)) for _ in
                           range(self.queen_num)]
        return queen_positions

    # get the possible children from parent node
    def get_children(self):
        children = []
        parent_queen_positions = list(self.queen_positions)
        for queen_index, queen in enumerate(parent_queen_positions):
            new_positions = [(queen[0], row) for row in range(self.side_length) if row != queen[1]]
            for new_position in new_positions:
                queen_positions = deepcopy(parent_queen_positions)
                queen_positions[queen_index] = new_position
                children.append(QueensState(queen_positions))
        return children
    # A function to identify attacking queens
    def queen_attacks(self):

        def range_between(a, b):
            if a > b:
                return range(a-1, b, -1)
            elif a < b:
                return range(a+1, b)
            else:
                return [a]

        def zip_repeat(a, b):
            if len(a) == 1:
                a = a*len(b)
            elif len(b) == 1:
                b = b*len(a)
            return zip(a, b)

        def points_between(a, b):
            return zip_repeat(list(range_between(a[0], b[0])), list(range_between(a[1], b[1])))

        def is_attacking(queens, a, b):
            if (a[0] == b[0]) or (a[1] == b[1]) or (abs(a[0]-b[0]) == abs(a[1] - b[1])):
                for between in points_between(a, b):
                    if between in queens:
                        return False
                return True
            else:
                return False

        attacking_pairs = []
        queen_positions = list(self.queen_positions)
        left_to_check = deepcopy(queen_positions)
        while left_to_check:
            a = left_to_check.pop()
            for b in left_to_check:
                if is_attacking(queen_positions, a, b):
                    attacking_pairs.append([a, b])

        return attacking_pairs

    def num_queen_attacks(self):
        return len(self.queen_attacks())

    def __str__(self):
        return '\n'.join([' '.join(['0' if (col, row) not in self.queen_positions else 'Q' for col in range(
            self.side_length)]) for row in range(self.side_length)])

    def __hash__(self):
        return hash(self.queen_positions)

    def __eq__(self, other):
        return self.queen_positions == other.queen_positions

    def __lt__(self, other):
        return self.f_cost < other.f_cost or (self.f_cost == other.f_cost and self.id > other.id)

print("Please select the algorithm to be executed :\n 1. Steepest Ascent \n 2. Hill Climbing with Sideway Moves\n 3. Random Restart")
x=input()#Taking Input from User
def steepest_ascent_hill_climb_false(queens_state,counter,allow_sideways=False, max_sideways=100):
    # This function will get call when steepest Ascent Hill Climb without side moves is selected
    node = queens_state
    path = []
    sideways_moves = 0
    while True:
        path.append(node)
        children = node.get_children()
        children_num_queen_attacks = [child.num_queen_attacks() for child in children]
        min_queen_attacks = min(children_num_queen_attacks)
        # If best child is not chosen randomly from the set of children that have the lowest number of attacks,
        # algorithm will go into infinite loop
        best_child = choice([child for child_index, child in enumerate(children) if children_num_queen_attacks[
            child_index] == min_queen_attacks])# 'for' loop will check the best heuristic by iterating through the num of attacking moves related to particular child node.
        if (best_child.num_queen_attacks() > node.num_queen_attacks()):# If we found better heuristic then break
            break
        elif best_child.num_queen_attacks() == node.num_queen_attacks():
            if not allow_sideways or sideways_moves == max_sideways:# Check if allowed side moves reched to the limit or not.
                break
            else:
                sideways_moves += 1
        else:
            sideways_moves = 0
        node = best_child
        if counter <4:
            print('Search Sequence :',counter,'\n', best_child, '\n')# Print first three sequences found while finding the solution
    return {'outcome': 'success' if node.num_queen_attacks()==0 else 'failure',
            'solution': path}

def steepest_ascent_hill_climb_true(queens_state,counter,allow_sideways=True, max_sideways=100):
    # This function will get call when steepest Ascent Hill Climb with side moves is selected
    node = queens_state
    path = []
    sideways_moves = 0
    while True:
        path.append(node)
        children = node.get_children()
        children_num_queen_attacks = [child.num_queen_attacks() for child in children]
        min_queen_attacks = min(children_num_queen_attacks)
        # If best child is not chosen randomly from the set of children that have the lowest number of attacks,
        # algorithm will go into infinite loop
        best_child = choice([child for child_index, child in enumerate(children) if children_num_queen_attacks[
            child_index] == min_queen_attacks])
        if (best_child.num_queen_attacks() > node.num_queen_attacks()):
            break
        elif best_child.num_queen_attacks() == node.num_queen_attacks():
            if not allow_sideways or sideways_moves == max_sideways:
                break
            else:
                sideways_moves += 1
        else:
            sideways_moves = 0
        node = best_child
        if counter <4:
            print('Search Sequence :', counter, '\n', best_child, '\n')
            #print(best_child)
    return {'outcome': 'success' if node.num_queen_attacks()==0 else 'failure',
            'solution': path}

def steepest_ascent_hill_climb(queens_state,allow_sideways, max_sideways=100):
    node = queens_state
    path = []
    sideways_moves = 0
    while True:
        path.append(node)
        children = node.get_children()
        children_num_queen_attacks = [child.num_queen_attacks() for child in children]
        min_queen_attacks = min(children_num_queen_attacks)
        # If best child is not chosen randomly from the set of children that have the lowest number of attacks,
        # then algorithm will get stuck flip-flopping between two non-random best children when sideways moves are
        # allowed
        best_child = choice([child for child_index, child in enumerate(children) if children_num_queen_attacks[
            child_index] == min_queen_attacks])
        if (best_child.num_queen_attacks() > node.num_queen_attacks()):
            break
        elif best_child.num_queen_attacks() == node.num_queen_attacks():
            if not allow_sideways or sideways_moves == max_sideways:
                break
            else:
                sideways_moves += 1
        else:
            sideways_moves = 0
        node = best_child
    return {'outcome': 'success' if node.num_queen_attacks()==0 else 'failure',
            'solution': path}

def random_restart_hill_climb(random_state_generator,allow_sideways,num_restarts=100, max_sideways=100):
    path = []
    global total # Global Variable Declaration
    for _ in range(num_restarts):
        # Repeatedly do the steepest ascent hill climbing algorithm with or without side way moves for n number of iterations.
        result = steepest_ascent_hill_climb(random_state_generator(),allow_sideways=allow_sideways,
                                        max_sideways=max_sideways)
        path += result['solution']
        num_restarts -= 1
        temp =0
        if result['outcome'] == 'success':
            temp = 100-num_restarts #check the num of restarts required for particular iteration
            break
    result['solution'] = path
    array.append(temp)#Appending num of restarts required in an array.
    total = 0
    for i in array:
        total += i # Find the total, summation of restarts found in an arrray for particular iteration
    return result

class QueensProblem:
    global n,num_iter # Global Variable Declaration
    print("Enter the number of queens")
    n = input()#Taking number of queens required in NxN board, as a input from user
    print("Enter the number of interations")
    num_iter = input()#Number of iterations to be performed
    num_iter = int(num_iter)
    # print(n)
    def __init__(self, start_state=QueensState()):
        self.start_state = start_state

def stats(search_function,counter=1, num_iterations=num_iter):
    results = []
    for iter_num in range(num_iterations):
        result = search_function(QueensState(),counter)#Create the object of QueenState and call the function passed e.g steepest_ascent_hill_climb/steepest_ascent_hill_climb_false
        counter += 1
        result['path_length'] = len(result['solution'])-1#Storing the path length of each iteration in result
        results.append(result)
    arr = [[result for result in results if result['outcome'] == 'success'], #array arr will have all the result of SUCCESS and FAILURE
           [result for result in results if result['outcome'] == 'failure']]
    success = []
    failure = []

    for i in arr[0]:
        success.append(i['path_length'])#0th index of array is corresponding to Success. Append all elements in success array
    for i in arr[1]:
        failure.append(i['path_length'])#1st index of array is corresponding to Failure. Append all elements in failure array
    if len(success) != 0:
        #Print the average number of steps for success
        print('Average number of steps when it succeeds: ', int(round(sum(success) / float(len(success)))))
    if len(failure) != 0:
        # Print the average number of steps for failure
        print('Average number of steps when it fails: ', int(round(sum(failure) / float(len(failure)))))

    results = [results,
               [result for result in results if result['outcome'] == 'success'],
               [result for result in results if result['outcome'] == 'failure']]
    title_col_width = 30
    data_col_width = 15

    def print_data_row(row_title, data_string, data_func, results):
        #Print function to print in row column format
        nonlocal title_col_width, data_col_width
        row = (row_title + '\t').rjust(title_col_width)
        for result_group in results:
            row += data_string.format(**data_func(result_group)).ljust(data_col_width)
        print(row)

    print('\t'.rjust(title_col_width) +
          'All Problems'.ljust(data_col_width) +
          'Successes'.ljust(data_col_width) +
          'Failures'.ljust(data_col_width))

    #Call to print_data_flow function with total number of  and percent
    print_data_row('Number of Problems:',
                   '{count:.0f} ({percent:.1%})',
                   lambda x: {'count':len(x), 'percent': len(x)/num_iterations},
                   results)

section_break = '\n' + '_'*100 + '\n'

def stats_random(search_function, num_iterations=num_iter):
    results = []
    global array # Global Variable Declaration
    array = []
    for iter_num in range(num_iterations):
        result = search_function(QueensState())#Create the object of QueenState and call the function passed e.g steepest_ascent_hill_climb/steepest_ascent_hill_climb_false
        result['path_length'] = len(result['solution'])-1#Storing the path length of each iteration in result
        results.append(result)
    arr = [[result for result in results if result['outcome'] == 'success'],#array arr will have all the result of SUCCESS and FAILURE
           [result for result in results if result['outcome'] == 'failure']]
    success = []
    failure = []

    for i in arr[0]:
        success.append(i['path_length'])#0th index of array is corresponding to Success. Append all elements in success array
    for i in arr[1]:
        failure.append(i['path_length'])#1st index of array is corresponding to Failure. Append all elements in failure array
    if len(success) != 0:
        # Print the average number of steps for success
        print('Average number of steps when it succeeds: ', int(round(sum(success) / float(len(success)))))
    if len(failure) != 0:
        # Print the average number of steps for failure
        print('Average number of steps when it fails: ', int(round(sum(failure) / float(len(failure)))))

    print(' '*50 + '\r', end='', flush=True)

    results = [results,
               [result for result in results if result['outcome'] == 'success'],
               [result for result in results if result['outcome'] == 'failure']]
    #print(results[0])
    title_col_width = 30
    data_col_width = 15

    def print_data_row(row_title, data_string, data_func, results):
        nonlocal title_col_width, data_col_width
        row = (row_title + '\t').rjust(title_col_width)
        for result_group in results:
            row += data_string.format(**data_func(result_group)).ljust(data_col_width)
        print(row)

    print('Avg No. of Restarts Required: ', int((total / num_iterations)))
    print('\t'.rjust(title_col_width) +
          'All Problems'.ljust(data_col_width) +
          'Successes'.ljust(data_col_width) +
          'Failures'.ljust(data_col_width))

    print_data_row('Number of Problems:',
                   '{count:.0f} ({percent:.1%})',
                   lambda x: {'count':len(x), 'percent': len(x)/num_iterations},
                   results)

if x=='1':
    print('Steepest ascent hill climb:\n')
    stats(steepest_ascent_hill_climb_false)
    print(section_break)
elif x=='2':
    print('Hill Climbing with Sideway Moves (up to 100 consecutive sideways moves allowed):\n')
    stats(steepest_ascent_hill_climb_true)
    print(section_break)
else:
    print("******************* Random Restart without Sideway Moves ******************")
    print('Random_restart_hill_climb):\n')
    stats_random(lambda x: random_restart_hill_climb(QueensState, allow_sideways=False))
    print(section_break)
    print("******************* Random Restart with Sideway Moves ******************")
    print('Random_restart_hill_climb):\n')
    stats_random(lambda x: random_restart_hill_climb(QueensState, allow_sideways=True))
    print(section_break)