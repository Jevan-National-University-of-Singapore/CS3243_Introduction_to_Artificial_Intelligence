from collections import deque
import copy
import sys
#import time
#start_time = time.time()

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, name, pos):
        self.type = name
        self.pos = pos
        self.pos_x = pos_index(pos[0])
        self.pos_y = pos[1]

    def within_board(self, x, y, board_row, board_col):
        return x > -1 and x < board_col and y > -1 and y < board_row
        
    def King_threat(self, board_row, board_col, threats, obstacles):
        for y in range(3):
            for x in range(3):
                if self.within_board(self.pos_x - 1 + x, self.pos_y - 1 + y, board_row, board_col):
                    if (self.pos_x - 1 + x, self.pos_y - 1 + y) in obstacles:
                        break
                    else:
                        threats.add((self.pos_x - 1 + x, self.pos_y - 1 + y))
        threats.remove((self.pos_x, self.pos_y))
        return threats
                   
    def Bishop_threat(self, board_row, board_col, threats, obstacles):
        #top left
        for x in range(1, self.pos_x):
            for y in range(1, self.pos_y):
                if self.within_board(self.pos_x - x, self.pos_y - y, board_row, board_col) and x == y:
                    if (self.pos_x - x, self.pos_y - y) in obstacles:
                        break
                    else:
                        threats.add((self.pos_x - x, self.pos_y - y)) 
            else:
                continue
            break

        #top right
        for x in range(1, board_col - self.pos_x):
            for y in range(1, self.pos_y):
                if self.within_board(self.pos_x + x, self.pos_y - y, board_row, board_col) and x == y:
                    if (self.pos_x + x, self.pos_y - y) not in obstacles:
                        break
                    else:
                        threats.add((self.pos_x + x, self.pos_y - y)) 
            else:
                continue
            break

        #bottom left
        for x in range(1, self.pos_x):
            for y in range(1, board_row - self.pos_y):
                if self.within_board(self.pos_x - x, self.pos_y + y, board_row, board_col) and x == y:
                    if (self.pos_x - x, self.pos_y + y) in obstacles:
                        break
                    else:
                        threats.add((self.pos_x - x, self.pos_y + y))
            else:
                continue
            break

        #bottom right
        for x in range(1, board_col - self.pos_x):
            for y in range(1, board_row - self.pos_y):
                if self.within_board(self.pos_x + x, self.pos_y + y, board_row, board_col) and x == y:
                    if (self.pos_x + x, self.pos_y + y) in obstacles:
                        break
                    else:
                        threats.add((self.pos_x + x, self.pos_y + y)) 
            else:
                continue
            break

        return threats
             
    def Rook_threat(self, board_row, board_col, threats, obstacles):
        #vertical up
        for y in range(1, self.pos_y):
            if (self.pos_x, self.pos_y - y) in obstacles:
                break
            else:
                threats.add((self.pos_x, self.pos_y - y))

        #vertical down
        for y in range(1, board_row - self.pos_y):
            if (self.pos_x, self.pos_y + y) in obstacles:
                break
            else:
                threats.add((self.pos_x, self.pos_y + y))

        #horizontal left
        for x in range(1, self.pos_x):
            if (self.pos_x - x, self.pos_y) in obstacles:
                break
            else:
                threats.add((self.pos_x - x, self.pos_y))
            
        #horizontal right
        for x in range(1, board_col - self.pos_x):
            if (self.pos_x + x, self.pos_y) in obstacles:
                break
            else:
                threats.add((self.pos_x + x, self.pos_y))
            
        return threats
    
    def Queen_threat(self, board_row, board_col, threats, obstacles):
        threats = self.Rook_threat(board_row, board_col, threats, obstacles)
        threats = self.Bishop_threat(board_row, board_col, threats, obstacles)
        return threats
    
    def Knight_threat(self, board_row, board_col, threats, obstacles):
        threat = 0
        #left -> right, top -> bottom
        if self.within_board(self.pos_x - 2, self.pos_y - 1, board_row, board_col):
            threats.add((self.pos_x - 2, self.pos_y - 1))
                
        if self.within_board(self.pos_x - 1, self.pos_y - 2, board_row, board_col):
            threats.add((self.pos_x - 1, self.pos_y - 2))
                
        if self.within_board(self.pos_x + 1, self.pos_y - 2, board_row, board_col):
            threats.add((self.pos_x + 1, self.pos_y - 2))
                
        if self.within_board(self.pos_x + 2, self.pos_y - 1, board_row, board_col):
            threats.add((self.pos_x + 2, self.pos_y - 1))
            
        if self.within_board(self.pos_x - 2, self.pos_y + 1, board_row, board_col):
            threats.add((self.pos_x - 2, self.pos_y + 1))
                
        if self.within_board(self.pos_x - 1, self.pos_y + 2, board_row, board_col):
            threats.add((self.pos_x - 1, self.pos_y + 2))
                
        if self.within_board(self.pos_x + 1, self.pos_y + 2, board_row, board_col):
            threats.add((self.pos_x + 1, self.pos_y + 2))
                
        if self.within_board(self.pos_x + 2, self.pos_y + 1, board_row, board_col):
            threats.add((self.pos_x + 2, self.pos_y + 1))
                
        return threats

def pos_index(pos):
    return (ord(pos[0]) - 97)

def pos_tuple(pos):
    return pos[0], int(pos[1:])

def update_threats(piece, row, col, obstacles):
    if piece.type == "King":
        return piece.King_threat(row, col, set(), obstacles)
    elif piece.type == "Queen":
        return piece.Queen_threat(row, col, set(), obstacles)
    elif piece.type == "Bishop":
        return piece.Bishop_threat(row, col, set(), obstacles)
    elif piece.type == "Rook":
        return piece.Rook_threat(row, col, set(), obstacles)
    elif piece.type == "Knight":
        return piece.Knight_threat(row, col, set(), obstacles)

def update_pos(avail_pos, threats):
    for pos in threats:
        if pos in avail_pos:
            avail_pos.remove(pos)
    return avail_pos

def search(avail_pos, obstacles, num_of_pieces, row, column):
    return backtrack(avail_pos, obstacles, num_of_pieces, row, column, {})

def backtrack(avail_pos, obstacles, num_of_pieces, row, col, assignment):
    #assignment is complete
    if sum(num_of_pieces.values()) == 0:
        return assignment
    
    curr_piece = ""
    #select unassigned variable
    if num_of_pieces.get("Queen") != 0:
        curr_piece = "Queen"
    elif num_of_pieces.get("Bishop") != 0:
        curr_piece = "Bishop"
    elif num_of_pieces.get("Rook") != 0:
        curr_piece = "Rook"
    elif num_of_pieces.get("King") != 0:
        curr_piece = "King"
    elif num_of_pieces.get("Knight") != 0:
        curr_piece = "Knight"

    for x in avail_pos:
        #check if consistent
        pos = (chr(x[0] + 97), x[1])
        if x not in obstacles and assignment.get(pos) == None:
            piece = Piece(curr_piece, pos)
            assignment[pos] = curr_piece
            num_of_pieces[curr_piece] -= 1
            threats = update_threats(piece, row, col, obstacles)
            #inference
            not_threaten = True
            for piece_pos in assignment.keys():
                index_pos = (ord(piece_pos[0]) - 97, piece_pos[1])
                if index_pos in threats:
                    not_threaten = False
            if not_threaten:
                copy_avail_pos = copy.copy(avail_pos)
                copy_avail_pos.remove(x)
                copy_avail_pos = update_pos(copy_avail_pos, obstacles)
                result = backtrack(copy_avail_pos, obstacles, num_of_pieces, row, col, assignment)
                if result:
                    return result
            
            assignment.pop(pos)
            num_of_pieces[curr_piece] += 1
    return False

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    # testfile = sys.argv[1] #Do not remove. This is your input testfile.

    lines = deque()
    with open ('CSP1.txt') as f:
    #with open(testfile) as f:
        input_ = f.readlines()
    #store in queue
    for line in input_:
        lines.append(line.strip("\n"))
        
    row = int(lines.popleft().split(":")[1])
    col = int(lines.popleft().split(":")[1])
    
    num_obstacles = int(lines.popleft().split(":")[1])
    obstacles_pos = lines.popleft().split(":")[1].split()

    obstacles = set()
    #place obstacles on board
    if num_obstacles != 0:
        for j in obstacles_pos:
            piece = Piece("Obstacle",pos_tuple(j))
            obstacles.add((piece.pos_x, piece.pos_y))

    #number of pieces to be placed on board
    pieces = lines.popleft().split(":")[1].split(' ')
    num_of_pieces = {}
    for i in range(0,5):
        if i == 0:
            num_of_pieces["King"] = int(pieces[i])
        elif i == 1:
            num_of_pieces["Queen"] = int(pieces[i])
        elif i == 2:
            num_of_pieces["Bishop"] = int(pieces[i])
        elif i == 3:
            num_of_pieces["Rook"] = int(pieces[i])
        elif i == 4:
            num_of_pieces["Knight"] = int(pieces[i])

    avail_pos = set()
    for y in range(row):
        for x in range(col):
            avail_pos.add((x,y))
    
    goalState = search(avail_pos, obstacles, num_of_pieces, row, col)
    return goalState #Format to be returned

print(run_CSP())
#print("--- %s seconds ---" % (time.time() - start_time))
