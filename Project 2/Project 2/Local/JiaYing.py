from collections import deque
import random
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
    
    def King(self, board):
        threat = -1
        for y in range(3):
            for x in range(3):
                if board.within(self.pos_x - 1 + x, self.pos_y - 1 + y):
                    if board.matrix[self.pos_y - 1 + y][self.pos_x - 1 + x] != ' ':
                        threat += 1

        return threat                      
                   
    def Bishop(self, board):
        threat = 0
        #top left
        for x in range(1, self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x - x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x - x] != ' ':
                        threat += 1

        #top right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, self.pos_y):
                if board.within(self.pos_x + x, self.pos_y - y) and x == y:
                    if board.matrix[self.pos_y - y][self.pos_x + x] != ' ':
                        threat += 1

        #bottom left
        for x in range(1, self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x - x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x - x] != ' ':
                        threat += 1

        #bottom right
        for x in range(1, board.columns - self.pos_x):
            for y in range(1, board.rows - self.pos_y):
                if board.within(self.pos_x + x, self.pos_y + y) and x == y:
                    if board.matrix[self.pos_y + y][self.pos_x + x] != ' ':
                        threat += 1

        return threat
             
    def Rook(self, board):
        threat = 0
        #vertical up
        for y in range(1, self.pos_y):
            if board.matrix[self.pos_y - y][self.pos_x] != ' ':
                threat += 1

        #vertical down
        for y in range(1, board.rows - self.pos_y):
            if board.matrix[self.pos_y + y][self.pos_x] != ' ':
                threat += 1

        #horizontal left
        for x in range(1, self.pos_x):
            if board.matrix[self.pos_y][self.pos_x - x] != ' ':
                threat += 1

        #horizontal right
        for x in range(1, board.columns - self.pos_x):
            if board.matrix[self.pos_y][self.pos_x + x] != ' ':
                threat +=1

        return threat
    
    def Queen(self, board):
        threat_rook = self.Rook(board)
        threat_bishop = self.Bishop(board)
        threat = threat_rook + threat_bishop
        return threat
    
    def Knight(self, board):
        threat = 0
        #left -> right, top -> bottom
        if board.within(self.pos_x - 2, self.pos_y - 1):
            if board.matrix[self.pos_y - 1][self.pos_x - 2] != ' ':
                threat += 1
                
        if board.within(self.pos_x - 1, self.pos_y - 2):
            if board.matrix[self.pos_y - 2][self.pos_x - 1] != ' ':
                threat += 1
                
        if board.within(self.pos_x + 1, self.pos_y - 2):
            if board.matrix[self.pos_y - 2][self.pos_x + 1] != ' ':
                threat += 1
                
        if board.within(self.pos_x + 2, self.pos_y - 1):
            if board.matrix[self.pos_y - 1][self.pos_x + 2] != ' ':
                threat += 1
            
        if board.within(self.pos_x - 2, self.pos_y + 1):
            if board.matrix[self.pos_y + 1][self.pos_x - 2] != ' ':
                threat += 1
                
        if board.within(self.pos_x - 1, self.pos_y + 2):
            if board.matrix[self.pos_y + 2][self.pos_x - 1] != ' ':
                threat += 1
                
        if board.within(self.pos_x + 1, self.pos_y + 2):
            if board.matrix[self.pos_y + 2][self.pos_x + 1] != ' ':
                threat += 1
                
        if board.within(self.pos_x + 2, self.pos_y + 1):
            if board.matrix[self.pos_y + 1][self.pos_x + 2] != ' ':
                threat += 1
                
        return threat

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

    def remove(self, piece):
        if piece.type == "King":
            self.matrix[piece.pos_y][piece.pos_x] = ' '
        elif piece.type == "Queen":
            self.matrix[piece.pos_y][piece.pos_x] = ' '
        elif piece.type == "Bishop":
            self.matrix[piece.pos_y][piece.pos_x] = ' '
        elif piece.type == "Rook":
            self.matrix[piece.pos_y][piece.pos_x] = ' '
        elif piece.type == "Knight":
            self.matrix[piece.pos_y][piece.pos_x] = ' '

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

    def print(self):
        for r in self.matrix:
            for c in r:
                if c == " ":
                    print("X ", end = "")
                print(f"{c.upper()[0:2]} ", end = "")
            print("")
        print("----------------------")

def pos_index(pos):
    if isinstance(pos,str):
        return ord(pos) - 97
    else:
        return int(pos)

def pos_tuple(pos):
    return pos[0], int(pos[1:])

def update_threats(board, list_of_pieces):
    dict_of_pieces = {}

    for piece in list_of_pieces:
        if piece.type == "King":
            num_of_threats = piece.King(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Queen":
            num_of_threats = piece.Queen(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Bishop":
            num_of_threats = piece.Bishop(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Rook":
            num_of_threats = piece.Rook(board)
            dict_of_pieces[piece] = num_of_threats
        elif piece.type == "Knight":
            num_of_threats = piece.Knight(board)
            dict_of_pieces[piece] = num_of_threats

    return dict_of_pieces

def num_of_threats(output):
    threats = 0
    for value in output.values():
        threats += value
    return threats

def search(board, pieces_pos, k):
    board.print()
    while True:
        output = {}
        new_board = board
        num_of_pieces = random.randrange(k,len(pieces_pos))
        list_of_pieces = random.sample(pieces_pos, num_of_pieces)
        for piece in list_of_pieces:
            new_board.place(piece)
            
        pieces_left = update_threats(new_board, list_of_pieces)

        if num_of_threats(pieces_left) == 0:
            for key in pieces_left.keys():
                output[key.pos] = key.type
            return output
            
        for i in range(0, num_of_pieces - k):
            #curr_piece = random.choice(list(pieces_left))
            maximum_value = -1
            maximum_pieces = {}
            for piece in pieces_left:
                if pieces_left[piece] > maximum_value:
                    maximum_pieces = {piece:pieces_left[piece]}
                elif pieces_left[piece] == maximum_value:
                    maximum_pieces[piece] = pieces_left[piece]
                
            curr_piece = random.choice(list(maximum_pieces.keys()))
            pieces_left.pop(curr_piece)
            new_board.remove(curr_piece)
            pieces_left = update_threats(new_board, pieces_left)
            if num_of_threats(pieces_left) == 0:
                for key in pieces_left.keys():
                    output[key.pos] = key.type
                return output

        
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    #testfile = sys.argv[1] #Do not remove. This is your input testfile.

    lines = deque()
    with open ('Local3.txt') as f:
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

    #board.print()
    min_pieces = int(lines.popleft().split(":")[1])
    pieces = lines.popleft()
    #find position of enemy pieces and place on board
    pieces_pos = []
    lines.popleft()
    while len(lines) > 0 and lines[0][0] == "[":
        piece = lines.popleft()[1:-1].split(",")
        pieces_pos.append(Piece(piece[0], pos_tuple(piece[1])))
        
    goalState = search(board, pieces_pos, min_pieces)
    return goalState #Format to be returned

print(run_local())
