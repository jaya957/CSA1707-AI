
"""
Simple 8-puzzle solver using A* search (Manhattan distance).
Input: nine integers 0..8 (0 is blank) separated by spaces.
Example input: 1 2 3 4 5 6 7 8 0
"""

from heapq import heappush, heappop

GOAL = (1,2,3,4,5,6,7,8,0)
NEIGHBORS = {
    0: [1,3],
    1: [0,2,4],
    2: [1,5],
    3: [0,4,6],
    4: [1,3,5,7],
    5: [2,4,8],
    6: [3,7],
    7: [4,6,8],
    8: [5,7]
}

def manhattan(state):
    """Manhattan distance of state from GOAL."""
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_index = val - 1  
        dist += abs(i//3 - goal_index//3) + abs(i%3 - goal_index%3)
    return dist

def is_solvable(state):
    """Check 8-puzzle solvability by counting inversions."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

def neighbors(state):
    z = state.index(0)
    for n in NEIGHBORS[z]:
        lst = list(state)
        lst[z], lst[n] = lst[n], lst[z]
        yield tuple(lst)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(start):
    """Return list of states from start to goal, or None if not found."""
    if start == GOAL:
        return [start]
    open_heap = []
    g_score = {start: 0}
    f_score = {start: manhattan(start)}
    heappush(open_heap, (f_score[start], 0, start))  # (f, tie-breaker, state)
    came_from = {}
    closed = set()
    tie = 0

    while open_heap:
        _, _, current = heappop(open_heap)
        if current == GOAL:
            return reconstruct_path(came_from, current)
        closed.add(current)

        for nb in neighbors(current):
            if nb in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, float('inf')):
                came_from[nb] = current
                g_score[nb] = tentative_g
                f = tentative_g + manhattan(nb)
                if nb not in [s for _,__,s in open_heap]:
                    tie += 1
                    heappush(open_heap, (f, tie, nb))
    return None

def print_state(state):
    for i in range(0,9,3):
        print(' '.join(str(x) if x!=0 else '_' for x in state[i:i+3]))
    print()

def main():
    try:
        s = input("Enter initial state (9 numbers 0..8, 0 = blank), separated by spaces:\n")
        parts = s.strip().split()
        if len(parts) != 9
