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

    nodes_expanded = 0
    max_queue_size = 1

    # main search loop
    while frontier:
        # track largest frontier size/memory usage
        max_queue_size = max(max_queue_size, len(frontier))

        # pop state with smallest f(n)
        f, g, state = heapq.heappop(frontier)

        print(f"The best state to expand with a g(n) = {g} and h(n) = {f - g} is…")
        print_board(state)

        if state == GOAL_STATE:
            print("Goal state reached!\n")
            print("Solution depth was", g)
            print("Number of nodes expanded:", nodes_expanded)
            print("Max queue size:", max_queue_size)
            return

        # if we've seen this state with a better cost, skip
        if state in explored and explored[state] <= g:
            continue

        explored[state] = g
        nodes_expanded += 1

        # expand neighbors
        for neighbor in get_neighbors(state):
# each move costs 1
            new_g = g + 1

            # if already explored with lower cost, skip
            if neighbor in explored and explored[neighbor] <= new_g:
                continue

            if heuristic_type == 1:
                new_h = 0
            elif heuristic_type == 2:
                new_h = misplaced_tile(neighbor)
            else:
                new_h = manhattan_distance(neighbor)

            heapq.heappush(frontier, (new_g + new_h, new_g, neighbor))

    # if queue empties without finding goal
    print("Failure: no solution found.")

# Driver Code

def main():

    # provided puzzles with known solution depths
    test_cases = {
        "0":  (1,2,3,4,5,6,7,8,0),
        "2":  (1,2,3,4,5,6,0,7,8),
        "4":  (1,2,3,5,0,6,4,7,8),
        "8":  (1,3,6,5,0,2,4,7,8),
        "12": (1,3,6,5,0,7,4,8,2),
        "16": (1,6,7,5,0,3,4,8,2),
        "20": (7,1,2,4,8,5,6,3,0),
        "24": (0,7,2,4,6,1,3,5,8)
    }

    print("Welcome to my 8-Puzzle Solver. Select a test case by depth:")
    for k in test_cases:
        print(f"Depth {k}")
    print("Or type 'custom' to enter your own.")

    choice = input("Choice: ")

    # for custom puzzle input
    if choice == "custom":
        print("Enter your puzzle row by row (use 0 for blank)")
        row1 = list(map(int, input("Row 1: ").split()))
        row2 = list(map(int, input("Row 2: ").split()))
        row3 = list(map(int, input("Row 3: ").split()))
        start_state = tuple(row1 + row2 + row3)
    else:
        start_state = test_cases[choice]

    print("\nSelect algorithm:")
    print("1) Uniform Cost Search")
    print("2) A* with Misplaced Tile Heuristic")
    print("3) A* with Manhattan Distance Heuristic")
    alg = int(input())

    general_search(start_state, alg)

if __name__ == "__main__":
    main()