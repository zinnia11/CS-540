import heapq
import math

def get_x(index):
    return index % 3

def get_y(index):
    return math.trunc(index/3)


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for i in range(len(from_state)):
        if (from_state[i] == 0):
            continue
        xindex = get_x(i)
        yindex = get_y(i)
        to_x = get_x(to_state.index(from_state[i]))
        to_y = get_y(to_state.index(from_state[i]))
        distance = distance + abs(xindex-to_x) + abs(yindex - to_y)

    return distance


def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle
        (don't forget to sort the result as done below). 
    """
    # if next to a empty space, then can move one over
    # same row index (x) and column index (y) can move
    succ_states = []

    # find blanks
    blanks = []
    for i in range(len(state)):
        if (state[i] == 0):
            blanks.append(i)

    new_state = state.copy()
    for b in blanks:
        xblank = get_x(b)
        yblank = get_y(b)
        # move same row 
        x = xblank - 1
        if (x>=0):
            index = b-1 # get the list index of the new x value
            if (state[index] != 0):
                new_state[b] = state[index] # blank and index swap
                new_state[index] = 0
                succ_states.append(new_state)
                new_state = state.copy()
        x = xblank + 1
        if (x<3):
            index = b+1
            if (state[index] != 0):
                new_state[b] = state[index] # blank and index swap
                new_state[index] = 0
                succ_states.append(new_state)
                new_state = state.copy()
        # move same column
        y = yblank - 1
        if (y>=0):
            index = b-3
            if (state[index] != 0):
                new_state[b] = state[index] # blank and index swap
                new_state[index] = 0
                succ_states.append(new_state)
                new_state = state.copy()
        y = yblank + 1
        if (y<3):
            index = b+3
            if (state[index] != 0):
                new_state[b] = state[index] # blank and index swap
                new_state[index] = 0
                succ_states.append(new_state)
                new_state = state.copy()
   
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along 
        h values, number of moves, and max queue number in the format specified in the pdf.
    """
    length = 0
    pq = [] # priority queue
    potential = [] # potetial paths from parent to child
    visited = set() # set for visited states

    # initialize priority queue with given state
    h = get_manhattan_distance(state)
    moves = 0
    heapq.heappush(pq, (h+moves, state, (moves, h, -1)))

    while (len(pq) != 0): # while priority queue is not empty
        # update length
        if (len(pq)>length):
            length = len(pq)

        s = heapq.heappop(pq)
        st = s[1] # state of the chosen
        if (st == goal_state): # if state is the goal then break from loops
            potential.append(s)
            break
        visited.add(tuple(s[1])) # add popped element to closed set

        potential.append(s) 
        parent = potential[s[2][2]] # find parent using the index into potential
        moves = s[2][0] + 1 

        succ = get_succ(st) # get successors of chosen state
        for state in succ:
            if tuple(state) in visited: # if the state is in the closed set of visited states
                continue
            h = get_manhattan_distance(state) 
            heapq.heappush(pq, (h+moves, state, (moves, h, len(potential)-1))) # parent is the last element

    # trace back the parents
    current = potential[len(potential)-1]
    next = 0
    path = []
    while (next != -1):
        next = current[2][2]
        path.insert(0, current)
        current = potential[next]
    # print
    for i in range(len(path)):
        node = path[i]
        print(node[1], "h={}".format(node[2][1]), "moves: {}".format(i))
    print("Max queue length: {}".format(length))


if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()
