########################################### LAYOUT ###################################################
##                                                                                                  ##
##  1. Global imports, variables and functions               #T_GBL                                 ##
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
##                                                                                                  ##
##      - Node:                                 #T_NODE                                             ##
##          . previous()                                                                            ##
##          . getPath()                                                                             ##
##  =============================================================================================   ##
##  3. Functions:                                #T_FNC                                             ##
##      - search(): does the BFS                                                                    ##
##      - run_BFS(): parse the file and initialise the state and environment                        ##
##  =============================================================================================   ##
##  4. Main     #T_MAIN                                                                             ##
##                                                                                                  ##
######################################################################################################

##=================== GLOBAL FUNCTIONS START ==================             ####T_GBL
import sys
from collections import deque

def INT(character: str) -> int: ##converts alpabets to integers
    return ord(character)-97

def CHR(integer: int) -> str: ##converts integers to alphabets
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
    def __init__(self, x: str, y: str, pieceType: str):
        self._PIECE_TYPE = pieceType
        self._x = INT(x)
        self._y = int(y)
    
    def x(self) -> str:
        return CHR(self._x)
    
    def y(self) -> str:
        return str(self._y)

    def type(self):
        return self._PIECE_TYPE
    
    def position(self) -> str:
        return CHR(self._x) + str(self._y)

    @staticmethod
    def create(piece_type, piece_position) -> object:  #create corresponding Piece subclasses
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
        
    #--------------- KNIGHT CLASS START ---------------                         ####T_KNIGHT
class Knight(Piece):                        
    def __init__(self, x, y):
        super().__init__(x, y, "Knight")

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
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

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
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

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
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


    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
        blocked = board.blocked()
        for i in range(self._y-1, -1, -1):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))
        
        for i in range(self._y+1,board.rows()):
            if (CHR(self._x) + str(i)) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))

        for i in range(self._x-1, -1, -1):
            if (CHR(i) + str(self._y)) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))

        for i in range(self._x+1,board.columns()):
            if (CHR(i) + str(self._y)) in blocked:
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

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
        blocked = board.blocked()
        for i in range(self._y-1, -1, -1):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))
        
        for i in range(self._y+1,board.rows()):
            if CHR(self._x) + str(i) in blocked:
                break
            else:
                all_threats.add(CHR(self._x)+str(i))

        for i in range(self._x-1, -1, -1):
            if CHR(i) + str(self._y) in blocked:
                break
            else:
                all_threats.add(CHR(i)+str(self._y))

        for i in range(self._x+1,board.columns()):
            if CHR(i) + str(self._y) in blocked:
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
        self._ROWS: int = rows              #1-based       
        self._COLUMNS: int = columns        #1-based
        self._MAX_X: int = columns -1       #0-based
        self._MAX_Y: int = rows -1          #0-based
        self._obstacles: list = obstacles   #list of objects subclassed from Piece ## -> List[objects]
        self._enemy_pieces: list = enemy_pieces #list of strings representing position of each obstacle ## -> List[str]
        self._blocked = set()

        for obstacle in obstacles:
            self._blocked.add(obstacle)
        for enemy in enemy_pieces:
            self._blocked.add(enemy.position())

    def maxX(self):      #0-based
        return self._MAX_X

    def maxY(self):      #0-based
        return self._MAX_Y
    
    def rows(self):      #1-based
        return self._ROWS

    def columns(self):   #1-based
        return self._COLUMNS

    def pieces(self):
        return self._enemy_pieces

    def obstacles(self): 
        return self._obstacles
    
    def blocked(self):
        return self._blocked
    
    def checkWithinBoard(self, x: int, y: int) -> bool: #takes in int position values
        return 0 <= x <= self._MAX_X and 0 <= y <= self._MAX_Y

    def getAllThreats(self) -> set:
        threatened = set()
        for piece in self._enemy_pieces:
            threatened = piece.getThreats(threatened, self)
        return threatened
    
    def getLegalMovesPositions(self, x: int, y: int) -> list:   # takes in int position values  ## -> List[string]
        ''' Legal moves are moves within the board limits INCLUDING THREATENED POSITIONS. '''
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

    #--------------- NODE CLASS START ---------------              ####T_NODE
class Node:
    def __init__(self, position, previous=None):
        self._position: str = position
        self._previous: str = previous
    
    def previous(self):
        return self._previous
    
    def setPrevious(self, previous_node):
        self._previous = previous_node

    def getMove(self): # returns the testcase format for move   ## -> [(str, int), (str, int)]
        previous_position = (self._previous[0], int(self._previous[1:]))
        current_position = (self._position[0], int(self._position[1:]))
        return [previous_position, current_position]

    def getPath(self, visited_nodes):    # returns the testcase format for path   ## -> List[[(str, int), (str, int)]]
        current_node = self
        path = [self.getMove()]
        while current_node.previous() is not None:
            path.insert(0, current_node.getMove())
            current_node = visited_nodes[current_node.previous()]
        return path
    #--------------- NODE CLASS END ---------------

##========================== CLASSES END =========================

##========================== FUNCTIONS START ===========================   
def search(start, board, goals):    #bfs algorithm
    '''The algorithm for BFS.'''

    start_y_int = int(start[1:])
    threatened = board.getAllThreats()
    blocked = board.blocked()
    queue = deque([start])         #frontier
    visited_nodes = {start: Node(position=start, previous=None)}

    if start in threatened:
        return [], 1 #no solution
    elif start in goals: #check start is goal
        move = [(start[0], start_y_int)]
        return [move], 1
    #start is not goal

    while queue:                                            #algo start
        current_position = queue.popleft()     #get a frontier node
        current_x_int = INT(current_position[0])
        current_y_int = int(current_position[1:])
        for next_position in board.getLegalMovesPositions(current_x_int, current_y_int):    #get all legal moves i.e. within board
            if next_position not in visited_nodes:                                          #check not visited then continue
                visited_nodes[next_position] = Node(position=next_position, previous=current_position)        #add to visited on pop
                if next_position not in threatened and next_position not in blocked:        #if valid then add to frontier
                    queue.append(next_position)
                    if next_position in goals:      #goal test
                        return visited_nodes[next_position].getPath(visited_nodes), len(visited_nodes)

    return [],len(visited_nodes)

## ******************** !!defining main ************************
def run_BFS():                                                                        ####T_BFS
    """Definition of main function.

    1. Parsing of file and initialising of environment
    2. Run search()
    """
    FILE = READ(sys.argv[1])
    # FILE = READ("1.txt")

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
        enemies.append(Piece.create(enemy_type, enemy_position))
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