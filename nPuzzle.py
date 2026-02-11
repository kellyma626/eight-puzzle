import heapq  # min-heap used as our priority queue

# puzzle is 3x3
N = 3
# goal state is (1 to 8 and 0) where 0 is the blank tile
GOAL_STATE = tuple(list(range(1, N*N)) + [0])

# Helper Functions

# print the board in 3x3 format
def print_board(state):
    for i in range(0, N*N, N):
        print(list(state[i:i+N]))
    print()

# gets index of the blank
def get_blank_index(state):
    return state.index(0)

# swap two positions in the puzzle
def swap(state, i, j):
    temp = list(state)
    temp[i], temp[j] = temp[j], temp[i]
    return tuple(temp)

# generate all valid next states by moving the blank tile
def get_neighbors(state):
    neighbors = []
    blank = get_blank_index(state)

    row = blank // N
    col = blank % N

    # move blank up
    if row > 0:
        neighbors.append(swap(state, blank, blank - N))

    # move blank down
    if row < N - 1:
        neighbors.append(swap(state, blank, blank + N))

    # move blank left
    if col > 0:
        neighbors.append(swap(state, blank, blank - 1))

    # move blank right
    if col < N - 1:
        neighbors.append(swap(state, blank, blank + 1))

    return neighbors

# Heuristic Functions

# counts how many tiles don’t match their goal position
def misplaced_tile(state):
    count = 0
    for i in range(N*N):
        if state[i] != 0 and state[i] != GOAL_STATE[i]:
            count += 1
    return count

# sum of Manhattan distances for each tile
# distance = |row1-row2| + |col1-col2|
def manhattan_distance(state):
    distance = 0
    for i in range(N*N):
        if state[i] == 0:
            continue
        goal_index = GOAL_STATE.index(state[i])
        x1, y1 = i // N, i % N
        x2, y2 = goal_index // N, goal_index % N
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# General Search Algorithm

def general_search(start_state, heuristic_type):

    # frontier is a priority queue ordered by f(n)
    # each element is (f(n), g(n), state)
    frontier = []

    # explored keeps track of visited states
    # value stored is best g(n) seen so far
    explored = {}

    if heuristic_type == 1:
        h = 0
    elif heuristic_type == 2:
        h = misplaced_tile(start_state)
    else:
        h = manhattan_distance(start_state)

    heapq.heappush(frontier, (h, 0, start_state))

    # main search loop
    while frontier:
        f, g, state = heapq.heappop(frontier)

        print_board(state)

        if state == GOAL_STATE:
            print("Goal state reached!")
            return

        # if we've seen this state with a better cost, skip
        if state in explored and explored[state] <= g:
            continue

        explored[state] = g

        # expand neighbors
        for neighbor in get_neighbors(state):
            # each move costs 1
            new_g = g + 1

            if heuristic_type == 1:
                new_h = 0
            elif heuristic_type == 2:
                new_h = misplaced_tile(neighbor)
            else:
                new_h = manhattan_distance(neighbor)

            heapq.heappush(frontier, (new_g + new_h, new_g, neighbor))