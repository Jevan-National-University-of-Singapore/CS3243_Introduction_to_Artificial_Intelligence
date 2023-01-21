board = [ 
    [2, 3, -1],
    [1, 8, 4],
    [7, 6, 5]
]

goal = [ 
    [1, 2, 3],
    [8, -1, 4],
    [7, 6, 5]
]
start = [0,0]
for i in range(3):
    for j in range (3):
        if board[i][j] == -1:
            start[0] = j
            start[1] = i


def checkWithinBoard(position):
    if position[0]<0 or position[0]>2 or position[1]< 0 or position[1]>2:
        return False
    return True

def getLegalMoves(position):
    legalMoves = []
    dx = [-1, 0, 0, 1]
    dy = [0, -1, 1, 0]
    for i in range(4):
        if checkWithinBoard([position[0] + dx[i], position[1] + dy[i]]):
            legalMoves.append([position[0] + dx[i], position[1] + dy[i]])

    return legalMoves

def checkCost(board, goal):
    cost = 0
    for i in range(3):
        for j in range (3):
            if board[j][i] != goal[j][i]:
                cost += 1
    return cost

def descent():
    current_cost = checkCost(board, goal)
    current_blank = start
    sequence = [start]
    while True:
        min_cost = -1
        min_move = (-1, -1)
        for move in getLegalMoves(current_blank):
            board_copy = board.copy()
            current_x = current_blank[0]
            current_y = current_blank[1]
            x= move[0]
            y = move[1]
            board_copy[y][x], board_copy[current_y][current_x] = board_copy[current_y][current_x], board_copy[y][x]
            cost = checkCost(board_copy, goal)
            if cost <= current_cost:
                if min_cost < 0 or cost < min_cost:
                    min_cost = cost
                    min_move = move
        if min_cost < 0:
            break
        sequence.append(min_move)
        current_cost = min_cost
        current_blank = min_move

    print(sequence)

descent()

