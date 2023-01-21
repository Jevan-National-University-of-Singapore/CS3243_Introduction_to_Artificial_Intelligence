from collections import deque
import copy
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, name, pos):
        self.type = name
        self.pos = pos
        self.pos_x = pos_index(pos[0])
        self.pos_y = pos_index(pos[1])
    
    def King_threat(self, board):
        threat = -1
        for y in range(3):
            for x in range(3):
                if board.within(self.pos_x - 1 + x, self.pos_y - 1 + y):
                    if board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] != ' ' and board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] != 'x':
                        threat += 1
                    if board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] == "Obstacle":
                        threat -= 1

        return threat

    def King_board(self, board):
        for y in range(3):
            for x in range(3):
                if board.within(self.pos_x - 1 + x, self.pos_y - 1 + y):
                    if board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] == ' ':
                        board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] = 'x'
        return board
                   
    def Bishop_threat(self, board):
        threat = 0
        #top left
        for x in range(1, self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x - x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x - x] != ' ' and board.matrix[self.pos_y - y][self.pos_x - x] != 'x':
                        threat += 1
                    if board.matrix[self.pos_y - y][self.pos_x - x] == 'Obstacle':
                        threat -= 1
                        break 
            else:
                continue
            break

        #top right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x + x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x + x] != ' ' and board.matrix[self.pos_y - y][self.pos_x + x] != 'x':
                        threat += 1
                    if board.matrix[self.pos_y - y][self.pos_x + x] == 'Obstacle':
                        threat -= 1
                        break
            else:
                continue
            break

        #bottom left
        for x in range(1, self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x - x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x - x] != ' ' and board.matrix[self.pos_y + y][self.pos_x - x] != 'x':
                        threat += 1
                    if board.matrix[self.pos_y + y][self.pos_x - x] == 'Obstacle':
                        threat -= 1
                        break
            else:
                continue
            break

        #bottom right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x + x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x + x] != ' ' and board.matrix[self.pos_y + y][self.pos_x + x] != 'x':
                        threat += 1
                    if board.matrix[self.pos_y + y][self.pos_x + x] == 'Obstacle':
                        break
            else:
                continue
            break

        return threat

    def Bishop_board(self, board):
        #top left
        for x in range(1, self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x - x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x - x] == ' ':
                        board.matrix[self.pos_y - y][self.pos_x - x] = 'x'
                    elif board.matrix[self.pos_y - y][self.pos_x - x] != 'x':
                        break
            else:
                continue
            break

        #top right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x + x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x + x] == ' ':
                        board.matrix[self.pos_y - y][self.pos_x + x] = 'x'
                    elif board.matrix[self.pos_y - y][self.pos_x + x] != 'x':
                        break
            else:
                continue
            break

        #bottom left
        for x in range(1, self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x - x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x - x] == ' ':
                        board.matrix[self.pos_y + y][self.pos_x - x] = 'x'
                    elif board.matrix[self.pos_y + y][self.pos_x - x] != 'x':
                        break
            else:
                continue
            break

        #bottom right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x + x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x + x] == ' ':
                        board.matrix[self.pos_y + y][self.pos_x + x] = 'x'
                    elif board.matrix[self.pos_y + y][self.pos_x + x] != 'x':
                        break
            else:
                continue
            break

        return board
             
    def Rook_threat(self, board):
        threat = 0
        #vertical up
        for y in range(1, self.pos_y):
            if board.matrix[self.pos_y - y][self.pos_x] != ' ' and board.matrix[self.pos_y - y][self.pos_x] != 'x':
                threat += 1
            if board.matrix[self.pos_y - y][self.pos_x] == 'Obstacle':
                threat -= 1
                break

        #vertical down
        for y in range(1, board.rows - self.pos_y):
            if board.matrix[self.pos_y + y][self.pos_x] != ' ' and board.matrix[self.pos_y + y][self.pos_x] != 'x':
                threat += 1
            if board.matrix[self.pos_y + y][self.pos_x] == 'Obstacle':
                threat -= 1
                break

        #horizontal left
        for x in range(1, self.pos_x):
            if board.matrix[self.pos_y][self.pos_x - x] != ' ' and board.matrix[self.pos_y][self.pos_x - x] != 'x':
                threat += 1
            if board.matrix[self.pos_y][self.pos_x - x] == 'Obstacle':
                threat -= 1
                break
            
        #horizontal right
        for x in range(1, board.columns - self.pos_x):
            if board.matrix[self.pos_y][self.pos_x + x] != ' ' and board.matrix[self.pos_y][self.pos_x + x] != 'x':
                threat +=1
            if board.matrix[self.pos_y][self.pos_x + x] == 'Obstacle':
                threat -= 1
                break
            
        return threat

    def Rook_board(self, board):
        #vertical up
        for y in range(1, self.pos_y):
            if board.matrix[self.pos_y - y][self.pos_x] == ' ':
                board.matrix[self.pos_y - y][self.pos_x] = 'x'
            elif board.matrix[self.pos_y - y][self.pos_x] != 'x':
                break

        #vertical down
        for y in range(1, board.rows - self.pos_y):
            if board.matrix[self.pos_y + y][self.pos_x] == ' ':
                board.matrix[self.pos_y + y][self.pos_x] = 'x'
            elif board.matrix[self.pos_y + y][self.pos_x] != 'x':
                break

        #horizontal left
        for x in range(1, self.pos_x):
            if board.matrix[self.pos_y][self.pos_x - x] == ' ':
                board.matrix[self.pos_y][self.pos_x - x] = 'x'
            elif board.matrix[self.pos_y][self.pos_x - x] != 'x':
                break

        #horizontal right
        for x in range(1, board.columns - self.pos_x):
            if board.matrix[self.pos_y][self.pos_x + x] == ' ':
                board.matrix[self.pos_y][self.pos_x + x] = 'x'
            elif board.matrix[self.pos_y][self.pos_x + x] != 'x':
                break

        return board
    
    def Queen_threat(self, board):
        threat_rook = self.Rook_threat(board)
        threat_bishop = self.Bishop_threat(board)
        threat = threat_rook + threat_bishop
        return threat

    def Queen_board(self, board):
        board = self.Rook_board(board)
        board = self.Bishop_board(board)
        return board
    
    def Knight_threat(self, board):
        threat = 0
        #left -> right, top -> bottom
        if board.within(self.pos_x - 2, self.pos_y - 1):
            if board.matrix[self.pos_y - 1][self.pos_x - 2] != ' ' and board.matrix[self.pos_y - 1][self.pos_x - 2] != 'x':
                threat += 1
            if board.matrix[self.pos_y - 1][self.pos_x - 2] == 'Obstacle':
                threat -= 1
            
                
        if board.within(self.pos_x - 1, self.pos_y - 2):
            if board.matrix[self.pos_y - 2][self.pos_x - 1] != ' ' and board.matrix[self.pos_y - 2][self.pos_x - 1] != 'x':
                threat += 1
            if board.matrix[self.pos_y - 2][self.pos_x - 1] == 'Obstacle':
                threat -= 1
                
        if board.within(self.pos_x + 1, self.pos_y - 2):
            if board.matrix[self.pos_y - 2][self.pos_x + 1] != ' ' and board.matrix[self.pos_y - 2][self.pos_x + 1] != 'x':
                threat += 1
            if board.matrix[self.pos_y - 2][self.pos_x + 1] == 'Obstacle':
                threat -= 1
                
        if board.within(self.pos_x + 2, self.pos_y - 1):
            if board.matrix[self.pos_y - 1][self.pos_x + 2] != ' ' and board.matrix[self.pos_y - 1][self.pos_x + 2] != 'x':
                threat += 1
            if board.matrix[self.pos_y - 1][self.pos_x + 2] == 'Obstacle':
                threat -= 1
            
        if board.within(self.pos_x - 2, self.pos_y + 1):
            if board.matrix[self.pos_y + 1][self.pos_x - 2] != ' ' and board.matrix[self.pos_y + 1][self.pos_x - 2] != 'x':
                threat += 1
            if board.matrix[self.pos_y + 1][self.pos_x - 2] == 'Obstacle':
                threat -= 1
                
        if board.within(self.pos_x - 1, self.pos_y + 2):
            if board.matrix[self.pos_y + 2][self.pos_x - 1] != ' ' and board.matrix[self.pos_y + 2][self.pos_x - 1] != 'x':
                threat += 1
            if board.matrix[self.pos_y + 2][self.pos_x - 1] == 'Obstacle':
                threat -= 1
                
        if board.within(self.pos_x + 1, self.pos_y + 2):
            if board.matrix[self.pos_y + 2][self.pos_x + 1] != ' ' and board.matrix[self.pos_y + 2][self.pos_x + 1] != 'x':
                threat += 1
            if board.matrix[self.pos_y + 2][self.pos_x + 1] == 'Obstacle':
                threat -= 1
                
        if board.within(self.pos_x + 2, self.pos_y + 1):
            if board.matrix[self.pos_y + 1][self.pos_x + 2] != ' ' and board.matrix[self.pos_y + 1][self.pos_x + 2] != 'x':
                threat += 1
            if board.matrix[self.pos_y + 1][self.pos_x + 2] == 'Obstacle':
                threat -= 1
                
        return threat

    def Knight_board(self, board):
        #left -> right, top -> bottom
        if board.within(self.pos_x - 2, self.pos_y - 1) and board.matrix[self.pos_y - 1][self.pos_x - 2] != 'x':
            if board.matrix[self.pos_y - 1][self.pos_x - 2] == ' ':
                board.matrix[self.pos_y - 1][self.pos_x - 2] = 'x'
                
        if board.within(self.pos_x - 1, self.pos_y - 2) and board.matrix[self.pos_y - 2][self.pos_x - 1] != 'x':
            if board.matrix[self.pos_y - 2][self.pos_x - 1] == ' ':
                board.matrix[self.pos_y - 2][self.pos_x - 1] = 'x'
                
        if board.within(self.pos_x + 1, self.pos_y - 2) and board.matrix[self.pos_y - 2][self.pos_x + 1] != 'x':
            if board.matrix[self.pos_y - 2][self.pos_x + 1] == ' ':
                board.matrix[self.pos_y - 2][self.pos_x + 1] = 'x'
                
        if board.within(self.pos_x + 2, self.pos_y - 1) and board.matrix[self.pos_y - 1][self.pos_x + 2] != 'x':
            if board.matrix[self.pos_y - 1][self.pos_x + 2] == ' ':
                board.matrix[self.pos_y - 1][self.pos_x + 2] = 'x'
            
        if board.within(self.pos_x - 2, self.pos_y + 1) and board.matrix[self.pos_y + 1][self.pos_x - 2] != 'x':
            if board.matrix[self.pos_y + 1][self.pos_x - 2] == ' ':
                board.matrix[self.pos_y + 1][self.pos_x - 2] = 'x'
                
        if board.within(self.pos_x - 1, self.pos_y + 2) and board.matrix[self.pos_y + 2][self.pos_x - 1] != 'x':
            if board.matrix[self.pos_y + 2][self.pos_x - 1] == ' ':
                board.matrix[self.pos_y + 2][self.pos_x - 1] = 'x'
                
        if board.within(self.pos_x + 1, self.pos_y + 2) and board.matrix[self.pos_y + 2][self.pos_x + 1] != 'x':
            if board.matrix[self.pos_y + 2][self.pos_x + 1] == ' ':
                board.matrix[self.pos_y + 2][self.pos_x + 1] = 'x'
                
        if board.within(self.pos_x + 2, self.pos_y + 1) and board.matrix[self.pos_y + 1][self.pos_x + 2] != 'x':
            if board.matrix[self.pos_y + 1][self.pos_x + 2] == ' ':
                board.matrix[self.pos_y + 1][self.pos_x + 2] = 'x'
                
        return board

class Board:
    def __init__(self, x, y):
        self.columns = x
        self.rows = y
        self.matrix = []
        for i in range(y):
            Row = []
            for j in range(x):
                Row.append(' ')
            self.matrix.append(Row)

    def place(self, piece):
        if piece.type == "King":
            self.matrix[piece.pos_y][piece.pos_x] = "King"
        elif piece.type == "Queen":
            self.matrix[piece.pos_y][piece.pos_x] = "Queen"
        elif piece.type == "Bishop":
            self.matrix[piece.pos_y][piece.pos_x] = "Bishop"
        elif piece.type == "Rook":
            self.matrix[piece.pos_y][piece.pos_x] = "Rook"
        elif piece.type == "Knight":
            self.matrix[piece.pos_y][piece.pos_x] = "Knight"
        elif piece.type == "Obstacle":
            self.matrix[piece.pos_y][piece.pos_x] = "Obstacle"

    def within(self, pos_x, pos_y):
        return pos_x > -1 and pos_x < self.columns and pos_y > -1 and pos_y < self.rows
    
    def valid_pos(self, pos_x, pos_y):
        lst_of_pos = {}
        for y in range(3):
            for x in range(3):
                if self.within(pos_x - 1 + x, pos_y - 1 + y):
                    if self.matrix[pos_y - 1 + y][pos_x - 1 + x] == ' ':
                        lst_of_pos[(chr(pos_x - 1 + x + 97),pos_y - 1 + y)] = 1
        return lst_of_pos

def pos_index(pos):
    if isinstance(pos,str):
        return ord(pos) - 97
    else:
        return int(pos)

def pos_tuple(pos):
    return pos[0], int(pos[1:])

def threaten(board, piece):
    if piece.type == "King":
        return piece.King_board(board)
    elif piece.type == "Queen":
        return piece.Queen_board(board)
    elif piece.type == "Bishop":
        return piece.Bishop_board(board)
    elif piece.type == "Rook":
        return piece.Rook_board(board)
    elif piece.type == "Knight":
        return piece.Knight_board(board)
    
def update_threats(board, list_of_pieces):
    dict_of_pieces = {}
    for key, value in list_of_pieces.items():
        piece = Piece(value, key)
        if piece.type == "King":
            num_of_threats = piece.King_threat(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Queen":
            num_of_threats = piece.Queen_threat(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Bishop":
            num_of_threats = piece.Bishop_threat(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Rook":
            num_of_threats = piece.Rook_threat(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Knight":
            num_of_threats = piece.Knight_threat(board)
            dict_of_pieces[piece] = num_of_threats
    return dict_of_pieces

def search(list_board, num_of_pieces):
    return backtrack(list_board, num_of_pieces, {})

def backtrack(list_board, num_of_pieces, assignment):
    print(sum(num_of_pieces.values()))
    #assignment is complete
    if sum(num_of_pieces.values()) == 0:
        return assignment
    
    curr_piece = ""
    #select unassigned variable
    if len(curr_piece) == 0:
        if num_of_pieces.get("Queen") != 0:
            # num_of_pieces["Queen"] = num_of_pieces.get("Queen") - 1
            curr_piece = "Queen"
        elif num_of_pieces.get("Bishop") != 0:
            # num_of_pieces["Bishop"] = num_of_pieces.get("Bishop") - 1
            curr_piece = "Bishop"
        elif num_of_pieces.get("Rook") != 0:
            # num_of_pieces["Rook"] = num_of_pieces.get("Rook") - 1
            curr_piece = "Rook"
        elif num_of_pieces.get("King") != 0:
            # num_of_pieces["King"] = num_of_pieces.get("King") - 1
            curr_piece = "King"
        elif num_of_pieces.get("Knight") != 0:
            # num_of_pieces["Knight"] = num_of_pieces.get("Knight") - 1
            curr_piece = "Knight"
            
    y_index = 0
    var = len(assignment)
    num_of_pieces[curr_piece] -= 1
    for y in list_board[var].matrix[0]:
        print(f"y: {y}")
        x_index = 0
        for x in y:
            print(f"x: {x}")
            #check if consistent
            if list_board[var].matrix[y_index][x_index] == ' ':
                new_board = copy.deepcopy(list_board[var])
                pos = (chr(x_index + 97), y_index)
                piece = Piece(curr_piece, pos)
                new_board.place(piece)
                new_board = threaten(new_board, piece)
                assignment[pos] = curr_piece
                inference = update_threats(new_board, assignment)

                if sum(inference.values()) == 0:
                    list_board.append(new_board)
                    result = backtrack(list_board, num_of_pieces, assignment)
                    if result:
                        return result
                    list_board.pop()
                print(assignment)
                assignment.pop(pos)
            x_index += 1
        y_index += 1
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
    column = int(lines.popleft().split(":")[1])
    board = Board(column, row)
    
    obstacles = int(lines.popleft().split(":")[1])
    obstacles_pos = lines.popleft().split(":")[1].split()

    #place obstacles on board
    if obstacles != 0:
        for j in obstacles_pos:
            piece = Piece("Obstacle",pos_tuple(j))
            board.place(piece)

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
    
    goalState = search([board], num_of_pieces)
    return goalState #Format to be returned

print(run_CSP())
