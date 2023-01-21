##############################************* LAYOUT ************#######################################
##                                                                                                  ##
##  1. Global variables and functions               #T_GBL                                          ##
##      - INT(): converts alphabets to integers                                                     ##
##      - CHR(): converts integers to alphabets                                                     ##
##      - READ(): returns a generator for reading files                                             ##
##  =============================================================================================   ##
##  2. Classes: #T_CLASS                                                                            ##
##      - Piece:                                                                                    ##
##          .Knight                             #T_KNIGHT                                           ##
##          .King                               #T_KING                                             ##
##          .Bishop                             #T_Bishop                                           ##
##          .Queen                              #T_QUEEN                                            ##
##          .Rook                               #T_ROOK                                             ##
##          .Obstacle(unused)                                                                       ##
##                                                                                                  ##
##      - Board:                                #T_BOARD                                            ##
##          . getBlocked()                                                                          ##
##          . getAllThreats()                                                                       ##
##  =============================================================================================   ##
##  3. Functions:                                #T_FNC                                             ##
##      - piece(): creates the chess piece and returns the created chess piece                      ##
##      - search(): does the BFS search                                                             ##
##      - run_BFS(): parse the file and initialise the state and environment                        ##
##  =============================================================================================   ##
##  4. Main     #T_MAIN                                                                             ##
##                                                                                                  ##
######################################################################################################

##=================== GLOBAL FUNCTIONS START ==================             ####T_GBL
import sys


def INT(character): ##converts alpabets to integers
    return ord(character)-97

def CHR(integer): ##converts integers to alphabets
    return chr(integer+97)

def READ(file_name): ## generator to read files
    lines = []
    with open(file_name) as f:
        lines = f.readlines()
    for line in lines:
        yield line.strip('\n')

##==================== GLOBAL FUNCTIONS END ====================
##========================= CLASSES START ======================================= ####T_CLASS
class Piece:                      # base class                                  ####T_PIECE
    def __init__(self, x, y, pieceType):
        self._PIECE_TYPE = pieceType
        self._x = INT(x)
        self._y = int(y)
    
    def x(self):
        return CHR(self._x)
    
    def y(self):
        return str(self._y)

    def type(self):
        return self._PIECE_TYPE
    
    def position(self):
        return CHR(self._x) + str(self._y)
        
    #--------------- KNIGHT CLASS START ---------------                         ####T_KNIGHT
class Knight(Piece):                        
    def __init__(self, x, y):
        super().__init__(x, y, "Knight")

    def getThreats(self, all_threats, board):
        blocked = board.blocked()
        if board.checkWithinBoard(self._x-2, self._y-1) and ((CHR(self._x-2) + str(self._y-1)) not in blocked):
            all_threats.add(CHR(self._x-2) + str(self._y-1))

        if board.checkWithinBoard(self._x-1, self._y-2) and ((CHR(self._x-1) + str(self._y-2)) not in blocked):
            all_threats.add(CHR(self._x-1) + str(self._y-2))
        
        if board.checkWithinBoard(self._x+2, self._y-1) and ((CHR(self._x+2) + str(self._y-1)) not in blocked):
            all_threats.add(CHR(self._x+2) + str(self._y-1))

        if board.checkWithinBoard(self._x+1, self._y-2) and ((CHR(self._x+1) + str(self._y-2)) not in blocked):
            all_threats.add(CHR(self._x+1) + str(self._y-2))

        if board.checkWithinBoard(self._x-1, self._y+2) and ((CHR(self._x-1) + str(self._y+2)) not in blocked):
            all_threats.add(CHR(self._x-1) + str(self._y+2))

        if board.checkWithinBoard(self._x-2, self._y+1) and ((CHR(self._x-2) + str(self._y+1)) not in blocked):
            all_threats.add(CHR(self._x-2) + str(self._y+1))

        if board.checkWithinBoard(self._x+1, self._y+2) and ((CHR(self._x+1) + str(self._y+2)) not in blocked):
            all_threats.add(CHR(self._x+1) + str(self._y+2))

        if board.checkWithinBoard(self._x+2, self._y+1) and ((CHR(self._x+2) + str(self._y+1)) not in blocked):
            all_threats.add(CHR(self._x+2) + str(self._y+1))
        return all_threats
    #--------------- KNIGHT CLASS END -----------------

    #--------------- KING CLASS START ---------------                         ####T_KING
class King(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "King")

    def getThreats(self, all_threats, board):
        blocked = board.blocked()
        if board.checkWithinBoard(self._x-1, self._y-1) and ((CHR(self._x- 1) + str(self._y -1)) not in blocked):
            all_threats.add(CHR(self._x- 1) + str(self._y -1))

        if board.checkWithinBoard(self._x-1, self._y) and ((CHR(self._x - 1) + str(self._y)) not in blocked):
            all_threats.add(CHR(self._x - 1) + str(self._y))

        if board.checkWithinBoard(self._x-1, self._y+1) and ((CHR(self._x- 1) + str(self._y+ 1)) not in blocked):
            all_threats.add(CHR(self._x- 1) + str(self._y+ 1))

        if board.checkWithinBoard(self._x, self._y-1) and ((CHR(self._x) + str(self._y -1)) not in blocked):
            all_threats.add(CHR(self._x) + str(self._y -1))

        if board.checkWithinBoard(self._x, self._y+1) and ((CHR(self._x) + str(self._y + 1)) not in blocked):
            all_threats.add(CHR(self._x) + str(self._y + 1))

        if board.checkWithinBoard(self._x+1, self._y-1) and ((CHR(self._x+ 1) + str(self._y -1)) not in blocked):
            all_threats.add(CHR(self._x+ 1) + str(self._y -1))

        if board.checkWithinBoard(self._x+1, self._y) and ((CHR(self._x+ 1) + str(self._y)) not in blocked):
            all_threats.add(CHR(self._x+ 1) + str(self._y))

        if board.checkWithinBoard(self._x+1, self._y+1) and ((CHR(self._x+ 1) + str(self._y +1)) not in blocked):
            all_threats.add(CHR(self._x+ 1) + str(self._y +1))
        return all_threats
    #---------------- KING CLASS END -----------------

    #--------------- BISHOP CLASS START ---------------                         ####T_BISHOP
class Bishop(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "Bishop")

    def getThreats(self, all_threats, board):
        blocked = board.blocked()
        check_x = self._x - 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y) and ((CHR(check_x)+str(check_y)) not in blocked):
            all_threats.add(CHR(check_x) + str(check_y))
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y) and ((CHR(check_x)+str(check_y)) not in blocked):
            all_threats.add(CHR(check_x) + str(check_y))
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y) and ((CHR(check_x)+str(check_y)) not in blocked):
            all_threats.add(CHR(check_x) + str(check_y))
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y) and ((CHR(check_x)+str(check_y)) not in blocked):
            all_threats.add(CHR(check_x) + str(check_y))
            check_x += 1
            check_y += 1
        
        return all_threats
    #--------------- BISHOP CLASS END -----------------

    #--------------- QUEEN CLASS START ---------------                         ####T_QUEEN
class Queen(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "Queen")


    def getThreats(self, all_threats, board):
        blocked = board.blocked()
        for i in range(0, self._y):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))
        
        for i in range(self._y+1,board.rows()):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))

        for i in range(0, self._x):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))

        for i in range(self._x+1,board.columns()):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))

        check_x = self._x - 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y) and CHR(check_x)+str(check_y) not in blocked:
            all_threats.add(CHR(check_x) + str(check_y))
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y) and CHR(check_x)+str(check_y) not in blocked:
            all_threats.add(CHR(check_x) + str(check_y))
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y) and CHR(check_x)+str(check_y) not in blocked:
            all_threats.add(CHR(check_x) + str(check_y))
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y) and CHR(check_x)+str(check_y) not in blocked:
            all_threats.add(CHR(check_x) + str(check_y))
            check_x += 1
            check_y += 1
        
        return all_threats
    #--------------- QUEEN CLASS END -----------------

    #--------------- ROOK CLASS START ---------------                         ####T_ROOK          
class Rook(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "Rook")

    def getThreats(self, all_threats, board):
        blocked = board.blocked()
        for i in range(0, self._y):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))
        
        for i in range(self._y+1,board.rows()):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))

        for i in range(0, self._x):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))

        for i in range(self._x+1,board.columns()):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))
        
        return all_threats
    #--------------- KNIGHT CLASS END -----------------

    #--------------- *IGNORE START*--------------- 
'''
class Obstacle(Piece):
     pass
'''
    #--------------- *IGNORE END*------------------

    #--------------- BOARD CLASS START ---------------              ####T_BOARD
class Board:
    def __init__(self, rows, columns, enemy_pieces, obstacles):
        self._ROWS = rows
        self._COLUMNS = columns
        self._MAX_X = columns -1
        self._MAX_Y = rows -1
        self._obstacles = obstacles
        self._enemy_pieces = enemy_pieces
        self._blocked = set()
        for obstacle in obstacles:
            self._blocked.add(obstacle)
        for enemy in enemy_pieces:
            self._blocked.add(enemy.position())

    def maxX(self):
        return self._MAX_X

    def maxY(self):
        return self._MAX_Y
    
    def rows(self):
        return self._ROWS

    def columns(self):
        return self._COLUMNS

    def pieces(self):
        return self._enemy_pieces

    def obstacles(self):
        return self._obstacles
    
    def blocked(self):
        return self._blocked

    def checkWithinBoard(self, x, y):
        if x < 0: return False
        if x > self._MAX_X: return False
        if y < 0: return False
        if y > self._MAX_Y: return False
        return True

    def getAllThreats(self):
        threatened = set()
        for piece in self._enemy_pieces:
            threatened = piece.getThreats(threatened, self)
        # for obstacle in self._obstacles:
        #     threatened.add(obstacle)
        return threatened
    
    def getLegalMovesPositions(self, x, y):
        legal_moves_positions = []
        if self.checkWithinBoard(x-1, y-1):
            legal_moves_positions.append(CHR(x-1) + str(y-1))
        
        if self.checkWithinBoard(x-1, y):
            legal_moves_positions.append(CHR(x-1) + str(y))

        if self.checkWithinBoard(x-1, y+1):
            legal_moves_positions.append(CHR(x-1) + str(y+1))

        if self.checkWithinBoard(x, y-1):
            legal_moves_positions.append(CHR(x) + str(y-1))

        if self.checkWithinBoard(x, y+1):
            legal_moves_positions.append(CHR(x) + str(y+1))
        
        if self.checkWithinBoard(x+1, y-1):
            legal_moves_positions.append(CHR(x+1) + str(y-1))

        if self.checkWithinBoard(x+1, y):
            legal_moves_positions.append(CHR(x+1) + str(y))

        if self.checkWithinBoard(x+1, y+1):
            legal_moves_positions.append(CHR(x+1) + str(y+1))
        return legal_moves_positions
    #--------------- BOARD CLASS END ---------------

##========================== CLASSES END =========================

##========================== FUNCTIONS START ===========================
def piece(piece_type, piece_position):  #create corresponding piece class
    if piece_type == "King":
        return King(piece_position[0], piece_position[1:])
    if piece_type == "Knight":
        return Knight(piece_position[0], piece_position[1:])
    if piece_type == "Rook":
        return Rook(piece_position[0], piece_position[1:])
    if piece_type == "Bishop":
        return Bishop(piece_position[0], piece_position[1:])
    if piece_type == "Queen":
        return Queen(piece_position[0], piece_position[1:])
        

def search(start, board, goals):    #bfs algorithm
    start_x_int = INT(start[0])
    start_y_int = int(start[1:])
    threatened = board.getAllThreats()
    blocked = board.blocked()
    queue = []
    visited = {start}
    if start not in threatened: # check start is goal
        move = [(start[0], start_y_int)]
        if start in goals:
            return [move], 1

    for position in board.getLegalMovesPositions(start_x_int, start_y_int): # first iteration
        visited.add(position)
        if position not in threatened and position not in blocked:
            current_position = (start[0], start_y_int)
            next_position = (position[0], int(position[1:]))
            move = [current_position, next_position]
            queue.append([move]) 
            if position[0]+position[1:] in goals:
                return [move], len(visited)

    while queue:                                            # second iteration onwards
        current_path = queue.pop(0)
        current_position = current_path[-1][-1]
        current_x_int = INT(current_position[0])
        current_y_int = int(current_position[1])
        for position in board.getLegalMovesPositions(current_x_int, current_y_int):
            if position not in visited:
                visited.add(position)
                if position not in threatened and position not in blocked:
                    path_copy = current_path.copy()                     # copy to let current_path be constant for all positions
                    next_position = (position[0], int(position[1:]))
                    move = [current_position, next_position]
                    path_copy.append(move)
                    queue.append(path_copy)
                    if next_position[0]+str(position[1:]) in goals:
                        return path_copy, len(visited)

    return [],len(visited)

## ******************** !!defining main ************************
def run_BFS():                  #main definition: parsing of file and initialising environment       ####T_BFS
    FILE =READ(sys.argv[1])
    # FILE = READ("4.txt")

    rows = int(next(FILE).split(":")[1])

    columns = int(next(FILE).split(":")[1])

    next(FILE) # burn ## number of obstacles (redundant)
    obstacles = next(FILE).split(":")[1].split()
    if obstacles[0] == "-" : 
        obstacles = []
    next(FILE) # burn ## step cost header
    while(next(FILE)[0] == "[" ): continue # burn action costs
    next(FILE) # burn 

    enemies = []
    enemy = next(FILE)
    while (enemy[0] == "["):
        enemy_type, enemy_position = enemy[1:-1].split(",")
        enemies.append(piece(enemy_type, enemy_position))
        enemy = next(FILE)

    next(FILE) # burn

    start = next(FILE)[1:-1].split(",")[1]
    goals = set()
    for goal_position in next(FILE).split(":")[1].split():
        goals.add(goal_position)
    FILE.close()

    return search(start, Board(rows, columns, enemies, obstacles), goals)
## ********************* end of main definition ************************
##============================= FUNCTIONS END =====================================

##======================= MAIN START ============================
# print(run_BFS())                                          #####T_MAIN