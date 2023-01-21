from queue import PriorityQueue
import heapq
import sys
# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, t, row, column, c=1, prev=None):
        self.type = t
        self.row = row
        self.column = column
        self.cost = c
        self.prev = prev

    def addCost(self, c):
        self.cost = c
    
    def changeType(self, t):
        self.type = t
    
    def addPrev(self, piece):
        self.prev = piece
    
    def __repr__(self):
        return "<%s, %s, (%s, %s)>" % (self.type, self.cost, self.row, self.column)


class Board:
    #populate the board with Empty space
    def __init__(self, row, col): 
        self.row = row
        self.col = col   
        self.board = []
        for i in range(row):
            row = []
            for j in range(col):
                row.append(Piece("Empty", i, j))
            self.board.append(row)

    def blockedPosition(self, row, col, piece_type):
        self.board[row][col].changeType(piece_type)
        if piece_type == "King":
            row_movement = [1, -1, 0, 0, 1, 1, -1, -1]
            col_movement = [0, 0, 1, -1, 1, -1, 1, -1]
            for i in range(8):
                new_row = row + row_movement[i]
                new_col = col + col_movement[i]
                if (0 <= new_row < self.row) and (0 <= new_col < self.col): 
                        if (self.board[new_row][new_col].type == "Empty"):
                            self.board[new_row][new_col].changeType("Blocked")
                        elif self.board[new_row][new_col].type == "Blocked":
                            continue
        elif piece_type == "Knight":
            row_movement = [-1, -2, -2, -1, 1, 2, 2, 1]
            col_movement = [-2, -1, 1, 2, -2, -1, 1, 2]
            for i in range(8):
                new_row = row + row_movement[i]
                new_col = col + col_movement[i]
                if (0 <= new_row < self.row) and (0 <= new_col < self.col):    
                    if (self.board[new_row][new_col].type == "Empty"):
                        self.board[new_row][new_col].changeType("Blocked")
                    elif self.board[new_row][new_col].type == "Blocked":
                        continue
        elif piece_type == "Rook":
            for i in range(row - 1, -1, -1):
                if (self.board[i][col].type == "Empty"):
                    self.board[i][col].changeType("Blocked")
                elif self.board[i][col].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(row + 1, self.row):
                if (self.board[i][col].type == "Empty"):
                    self.board[i][col].changeType("Blocked")
                elif self.board[i][col].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(col + 1, self.col):
                if (self.board[row][i].type == "Empty"):
                    self.board[row][i].changeType("Blocked")
                elif self.board[row][i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(col - 1, -1, -1):
                if (self.board[row][i].type == "Empty"):
                    self.board[row][i].changeType("Blocked")
                elif self.board[row][i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
        elif piece_type == "Bishop":
            smaller = min(row, col)
            for i in range(1, smaller + 1):
                if (self.board[row - i][col - i].type == "Empty"):
                    self.board[row - i][col - i].changeType("Blocked")
                elif self.board[row - i][col - i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(row, self.col - col - 1)
            for i in range(1, smaller + 1):
                if (self.board[row - i][col + i].type == "Empty"):
                    self.board[row - i][col + i].changeType("Blocked")
                elif self.board[row - i][col + i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(self.row - row - 1, col)
            for i in range(1, smaller + 1):
                if (self.board[row + i][col - i].type == "Empty"):
                    self.board[row + i][col - i].changeType("Blocked")
                elif self.board[row + i][col - i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(self.row - row - 1, self.col - col - 1)
            for i in range(1, smaller + 1):
                if (self.board[row + i][col + i].type == "Empty"):
                    self.board[row + i][col + i].changeType("Blocked")
                elif self.board[row + i][col + i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
        elif piece_type == "Queen":
            for i in range(row - 1, -1, -1):
                if (self.board[i][col].type == "Empty"):
                    self.board[i][col].changeType("Blocked")
                elif self.board[i][col].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(row + 1, self.row):
                if (self.board[i][col].type == "Empty"):
                    self.board[i][col].changeType("Blocked")
                elif self.board[i][col].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(col + 1, self.col):
                if (self.board[row][i].type == "Empty"):
                    self.board[row][i].changeType("Blocked")
                elif self.board[row][i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            for i in range(col - 1, -1, -1):
                if (self.board[row][i].type == "Empty"):
                    self.board[row][i].changeType("Blocked")
                elif self.board[row][i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(row, col)
            for i in range(1, smaller + 1):
                if (self.board[row - i][col - i].type == "Empty"):
                    self.board[row - i][col - i].changeType("Blocked")
                elif self.board[row - i][col - i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(row, self.col - col - 1)
            for i in range(1, smaller + 1):
                if (self.board[row - i][col + i].type == "Empty"):
                    self.board[row - i][col + i].changeType("Blocked")
                elif self.board[row - i][col + i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(self.row - row - 1, col)
            for i in range(1, smaller + 1):
                if (self.board[row + i][col - i].type == "Empty"):
                    self.board[row + i][col - i].changeType("Blocked")
                elif self.board[row + i][col - i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
            smaller = min(self.row - row - 1, self.col - col - 1)
            for i in range(1, smaller + 1):
                if (self.board[row + i][col + i].type == "Empty"):
                    self.board[row + i][col + i].changeType("Blocked")
                elif self.board[row + i][col + i].type != "Blocked":
                    break
                #     continue
                # else:
                #     break;
        
class State:
    pass

def switchBack(curr, next):
    m = []
    curr_col = chr(ord('a') + curr.column)
    next_col = chr(ord('a') + next.column)
    m.append((curr_col, curr.row))
    m.append((next_col, next.row))
    return m


def search(start, chessboard):
    nodes_explored = 0
    moves = []
    row_movement = [1, -1, 0, 0, 1, 1, -1, -1]
    col_movement = [0, 0, 1, -1, 1, -1, 1, -1]
    pq = []
    if chessboard.board[start[0]][start[1]].type == "Goal":
        return (moves, nodes_explored)
    heapq.heappush(pq, (0, start))
    visited = {start}
    pathCost = 0
    while pq:
        curr = heapq.heappop(pq)
        for i in range(8):
            row = curr[1][0] + row_movement[i]
            col = curr[1][1] + col_movement[i]
            if (0 <= row < chessboard.row) and (0 <= col < chessboard.col):
                if chessboard.board[row][col].type == "Goal":
                        curr = chessboard.board[row][col]
                        prev = chessboard.board[row][col].prev
                        while (prev != start):
                            #print(prev)
                            if prev == None:
                                break
                            else:
                                moves.append(switchBack(prev, curr))
                                pathCost += curr.cost
                                curr = prev
                                prev = prev.prev
                        moves.reverse()
                        pathCost = curr.cost 
                        return(moves, nodes_explored, pathCost)
                #print(row, col)
                if ((row, col) not in visited and (chessboard.board[row][col].type == "Empty" or chessboard.board[row][col].type == "Goal")):
                    visited.add((row, col))
                    nodes_explored += 1
                    chessboard.board[row][col].prev = chessboard.board[curr[1][0]][curr[1][1]]
                    print((row, col), chessboard.board[row][col].cost + chessboard.board[row][col].prev.cost)
                    heapq.heappush(pq, (chessboard.board[row][col].cost + chessboard.board[row][col].prev.cost, (row, col)))

    return(moves, nodes_explored, pathCost)



### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():

    # You can code in here but you cannot remove this function or change the return type
    # file_name = (sys.argv[1])
    file_name = "3.txt"
    f = open(file_name, "r")
    txt_file = f.read().split("\n")
    #creating the board
    row = int(txt_file[0].split(":")[1])
    col = int(txt_file[1].split(":")[1])
    chessboard = Board(row, col)
    #blocking out the obstacles
    obstacles = str(txt_file[3][38:]).split(' ')
    for obstacle in obstacles:
        #print(obstacle)
        row = int(obstacle[1:])
        col = ord(obstacle[0]) - ord('a')
        #print(row, col)
        chessboard.board[row][col].changeType('Obstacle')
    j = 5
    #addCost into the chessboard
    #print(len(txt_file))
    #print(txt_file[5])
    temp = []
    for i in range(5, len(txt_file)):
        #print(txt_file[i])
        if txt_file[i][0] == "[":
            #print('here')
            rowcol = txt_file[i].split(',')[0][1:]
            col = ord(rowcol[0]) - ord('a')
            row = int(rowcol[1:])
            #print((row,col))
            cost = int(txt_file[i].split(',')[1][0:-1])
            chessboard.board[row][col].addCost(cost)
            j += 1
        else:
            break
    #add enemy into the thing
    j += 2
    #print(txt_file[i][0])
    for i in range(j, len(txt_file)):
        if txt_file[i][0] == "[":
            opponent_type = txt_file[i].split(',')[0][1:]
            col = ord(txt_file[i].split(',')[1][0]) - ord('a')
            row = int(txt_file[i].split(",")[1][1:-1])
            temp.append([row, col, opponent_type])
            #chessboard.blockedPosition(row, col, opponent_type)
            chessboard.board[row][col].changeType(opponent_type)
            j += 1
        else:
            break
    for i in range(len(temp)):
        chessboard.blockedPosition(temp[i][0], temp[i][1], temp[i][2])
    #add start position
    j += 2
    start_col = ord(txt_file[j].split(',')[1][0]) - ord('a')
    start_row = int(txt_file[j].split(',')[1][1:-1])
    chessboard.board[start_row][start_col].changeType('Start')
    #add goal positions
    j += 1
    goals = txt_file[j].split(':')[1]
    allgoals = goals.split(' ')
    for goal in allgoals:
        col = ord(goal[0]) - ord('a')
        row = int(goal[1:])
        #print(row, col)
        chessboard.board[row][col].changeType('Goal')

    moves, nodesExplored, pathCost = search((start_row, start_col), chessboard) #For reference
    #print(chessboard.board)
    print(moves, nodesExplored, pathCost)

    return moves, nodesExplored, pathCost #Format to be returned
run_UCS()