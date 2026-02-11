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

# General Search Algorithm

def general_search(start_state):

    # frontier is a priority queue ordered by f(n)
    # each element is (f(n), g(n), state)
    frontier = []

    # explored keeps track of visited states
    explored = set()

    heapq.heappush(frontier, (0, 0, start_state))

    # main search loop
    while frontier:
        f, g, state = heapq.heappop(frontier)

        print_board(state)

        if state == GOAL_STATE:
            print("Goal state reached!")
            return

        if state in explored:
            continue

        explored.add(state)

        # expand neighbors
        for neighbor in get_neighbors(state):
            # each move costs 1
            new_g = g + 1
            heapq.heappush(frontier, (new_g, new_g, neighbor))