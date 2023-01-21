### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
import sys


def run_BFS():
    txtFile = "1.txt"#(sys.argv[1])
    ROWS = 0
    COLUMNS = 0
    OBSTACLES = []
    THREATHENED = {}
    ACTION_COSTS = {}
    GOALS = set()
    START = ""

    with open(txtFile) as f:
        lines = f.readlines()

        lines = [line.strip('\n') for line in lines]

        ROWS = int(lines[0][5:])
        COLUMNS = int(lines[1][5:])
        OBSTACLES = lines[3][38:].split(' ')
        for i in OBSTACLES:
            THREATHENED[i] = "O"

        current_line = 5
        for line in lines[5:-1]:
            if line[0] == "[":
                cost = line[1:-1].split(",")
                ACTION_COSTS[cost[0]]= int(cost[1])
                current_line += 1
            else:
                break
        
        numberOfEnemies = 0
        for i in lines[current_line][66:].split(" "):
            numberOfEnemies += int(i)
        
        current_line +=2
        for line in lines[current_line:current_line + numberOfEnemies]:
            enemy = line[1:-1].split(",")
            THREATHENED[enemy[1]] = enemy[0]
            x = ord(enemy[1][0]) - 97
            y = int(enemy[1][1:])
            if enemy[0] == "King":
                THREATHENED[chr(x - 1 + 97) + str(y -1)] = "King"
                THREATHENED[chr(x - 1 + 97) + str(y)] = "King"
                THREATHENED[chr(x - 1 + 97) + str(y + 1)] = "King"
                THREATHENED[chr(x + 97) + str(y -1)] = "King"
                THREATHENED[chr(x + 97) + str(y + 1)] = "King"
                THREATHENED[chr(x + 1 + 97) + str(y -1)] = "King"
                THREATHENED[chr(x + 1 + 97) + str(y)] = "King"
                THREATHENED[chr(x + 1 + 97) + str(y +1)] = "King"
            elif enemy[0] == "Knight":
                THREATHENED[chr(x-2 + 97) + str(y-1)] = "Knight"
                THREATHENED[chr(x-1+ 97) + str(y-2)] = "Knight"
                THREATHENED[chr(x+2+ 97) + str(y-1)] = "Knight"
                THREATHENED[chr(x+2+ 97) + str(y-1)] = "Knight"
                THREATHENED[chr(x-1+ 97) + str(y+2)] = "Knight"
                THREATHENED[chr(x-2+ 97) + str(y+1)] = "Knight"
                THREATHENED[chr(x+1+ 97) + str(y+2)] = "Knight"
                THREATHENED[chr(x+2+ 97) + str(y+1)] = "Knight"
                
            elif enemy[0] == "Rook":
                for i in range(0, y):
                    THREATHENED[chr(x+ 97)+str(i)] = "Rook"
                
                for i in range(y+1,ROWS):
                    THREATHENED[chr(x+ 97)+str(i) ] = "Rook"

                for i in range(0, x):
                    THREATHENED[chr(i+ 97)+str(y)] = "Rook"

                for i in range(x+1,COLUMNS):
                    THREATHENED[chr(i+ 97)+str(y)] = "Rook"
            
            elif enemy[0] == "Queen":
                for i in range(0, y):
                    THREATHENED[chr(x+ 97)+str(i)] = "Queen"
                
                for i in range(y+1,ROWS):
                    THREATHENED[chr(x+ 97)+str(i) ] = "Queen"

                for i in range(0, x):
                    THREATHENED[chr(i+ 97)+str(y)] = "Queen"

                for i in range(x+1,COLUMNS):
                    THREATHENED[chr(i+ 97)+str(y)] = "Queen"

                maxLength = max(ROWS, COLUMNS)
                for i in range(1,maxLength):
                    if (x - i < 0  or y <0):
                        break
                    else:
                        THREATHENED[chr(x - i + 97) + str(y-i)] = "Queen"

                for i in range(1, maxLength):
                    if (x - i < 0 or y  + i >= ROWS):
                        break
                    else:
                        THREATHENED[chr(x - i + 97) + str(y + i)] = "Queen"

                for i in range(1, maxLength):
                    if (x + i >= COLUMNS or y  - i < 0):
                        break
                    else:
                        THREATHENED[chr(x + i + 97) + str(y - i)] = "Queen"

                for i in range(1, maxLength):
                    if (x + i >= COLUMNS or y  + i >= ROWS):
                        break
                    else:
                        THREATHENED[chr(x + i + 97) + str(y + i)] = "Queen"

            elif enemy[0] == "Bishop":
                maxLength = max(ROWS, COLUMNS)
                for i in range(1,maxLength):
                    if (x - i < 0  or y <0):
                        break
                    else:
                        THREATHENED[chr(x - i + 97) + str(y-i)] = "Bishop"

                for i in range(1, maxLength):
                    if (x - i < 0 or y  + i >= ROWS):
                        break
                    else:
                        THREATHENED[chr(x - i + 97) + str(y + i)] = "Bishop"

                for i in range(1, maxLength):
                    if (x + i >= COLUMNS or y  - i < 0):
                        break
                    else:
                        THREATHENED[chr(x + i + 97) + str(y - i)] = "Bishop"

                for i in range(1, maxLength):
                    if (x + i >= COLUMNS or y  + i >= ROWS):
                        break
                    else:
                        THREATHENED[chr(x + i + 97) + str(y + i)] = "Bishop"
        current_line += numberOfEnemies + 2
        myPiece = lines[current_line][1:-1].split(",")
        START = myPiece[-1]
        goals = lines[-1][31:].split(" ")
        for goal in goals:
            GOALS.add(goal)


    queue = []
    print(THREATHENED.keys())

    x = ord(START[0])-97
    y = int(START[1:])
    visited = {START}
    possible_moves = []
    if x-1 >= 0 and x-1 < COLUMNS and y-1>=0 and y-1<ROWS:
        possible_moves.append(chr(x -1 +97) + str(y - 1))
    
    if x-1 >= 0 and x-1 < COLUMNS and y>=0 and y<ROWS:
        possible_moves.append(chr(x-1+97) + str(y))

    if x-1 >= 0 and x-1 < COLUMNS and y+1>=0 and y+1<ROWS:
        possible_moves.append(chr(x-1+97) + str(y+1))

    if x>= 0 and x<COLUMNS and y-1>=0 and y-1<ROWS:
        possible_moves.append(chr(x+97) + str(y - 1))

    if x>= 0 and x< COLUMNS and y+1>=0 and y+1<ROWS:
        possible_moves.append(chr(x+97) + str(y+1))

    if x+1 >= 0 and x+1 < COLUMNS and y-1>=0 and y-1<ROWS:
        possible_moves.append(chr(x+1+97) + str(y-1))

    if x+1 >= 0 and x+1 < COLUMNS and y>=0 and y<ROWS:
        possible_moves.append(chr(x+1+97) + str(y))
    
    if x+1 >= 0 and x+1 < COLUMNS and y+1>=0 and y+1<ROWS:
        possible_moves.append(chr(x +1+97) + str(y +1))

    for move in possible_moves:
        if ord(move[0]) - 97 >= 0 and ord(move[0]) - 97 < COLUMNS and int(move[1]) >= 0 and int(move[1]) < ROWS:
            if move not in THREATHENED:
                current_pos = (START[0], int(START[1:]))
                next_pos = (move[0], int(move[1:]))
                queue.append([[current_pos, next_pos]])
                visited.add(move)
                if move in GOALS:
                    return [[current_pos, next_pos]], len(visited)

    while queue:
        currentPath = queue.pop(0)
        currentPos = currentPath[-1][-1]

        x = ord(currentPos[0])-97
        y = currentPos[1]
        possible_moves = []
        if x-1 >= 0 and x-1 < COLUMNS and y-1>=0 and y-1<ROWS:
            possible_moves.append(chr(x -1+97) + str(y - 1))
        
        if x-1 >= 0 and x-1 < COLUMNS and y>=0 and y<ROWS:
            possible_moves.append(chr(x-1+97) + str(y))

        if x-1 >= 0 and x-1 < COLUMNS and y+1>=0 and y+1<ROWS:
            possible_moves.append(chr(x-1+97) + str(y+1))

        if x>= 0 and x<COLUMNS and y-1>=0 and y-1<ROWS:
            possible_moves.append(chr(x+97) + str(y - 1))

        if x>= 0 and x< COLUMNS and y+1>=0 and y+1<ROWS:
            possible_moves.append(chr(x+97) + str(y+1))

        if x+1 >= 0 and x+1 < COLUMNS and y-1>=0 and y-1<ROWS:
            possible_moves.append(chr(x+1+97) + str(y-1))

        if x+1 >= 0 and x+1 < COLUMNS and y>=0 and y<ROWS:
            possible_moves.append(chr(x+1+97) + str(y))
        
        if x+1 >= 0 and x+1 < COLUMNS and y+1>=0 and y+1<ROWS:
            possible_moves.append(chr(x +1+97) + str(y +1))

        # print(f"current pos: {currentPos}")

        # print("=================================")
        for move in possible_moves:
            # print(f"move[0]: {move[0]}")
            # print(f"move[1:]: {move[1:]}")
            if ord(move[0]) - 97 >= 0 and ord(move[0]) - 97 < COLUMNS and int(move[1:]) >= 0 and int(move[1:]) < ROWS:
                if move not in visited:
                    # print(f"move: {move}")
                    if move not in THREATHENED:
                        copy_path = currentPath.copy()
                        current_pos = (currentPos[0], y)
                        next_pos = (move[0], int(move[1:]))
                        copy_path.append([current_pos, next_pos])
                        queue.append(copy_path)
                        visited.add(move)
                        # print(f"move: {chr(int(move[0])+97) + move[1:]}")

                        if move in GOALS:
                            return copy_path, len(visited)

print(run_BFS())


