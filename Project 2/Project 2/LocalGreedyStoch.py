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
##          . getHeuristic()                                                                        ##
##          . printBoard()                                                                          ##
##                                                                                                  ##
##                                                                                                  ##
##  =============================================================================================   ##
##  3. Functions:                                #T_FNC                                             ##
##      - search(): does the local search                                                           ##
##      - run_local(): parse the file and initialise the state and environment                      ##
##  =============================================================================================   ##
##  4. Main     #T_MAIN                                                                             ##
##                                                                                                  ##
######################################################################################################

#LocalGreedyStoch

##=================== GLOBAL FUNCTIONS START ==================             ####T_GBL
from abc import abstractmethod
import sys
import heapq
import random
from time import time

NUM_OF_BEAMS = 1

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
    yield False

##==================== GLOBAL FUNCTIONS END ====================
##========================= CLASSES START ======================================= ####T_CLASS
class Piece:                      # base class                                  ####T_PIECE
    def __init__(self, x: str, y: str, pieceType: str, board: "Board"):
        self._PIECE_TYPE = pieceType
        self._x = INT(x)
        self._y = int(y)
        self._threats = self.getThreats(board)

    def __lt__(self, piece):
        return self._x < INT(piece.x())
    
    def __hash__(self):
        return hash((self._x, self._y))

    def __eq__(self, piece):
        return self._x == piece.x() and self._y == piece.y()

    def x(self) -> str:
        return CHR(self._x)
    
    def y(self) -> str:
        return str(self._y)

    def type(self):
        return self._PIECE_TYPE
    
    def position(self) -> str:
        return CHR(self._x) + str(self._y)

    def threats(self, piece_as_blocked = False) -> set:
        return self._threats
    
    @abstractmethod
    def getThreats(self, board: "Board", blocked_pieces = set()):
        pass

    @staticmethod
    def create(piece_type, piece_position, board: "Board") -> object:  #create corresponding Piece subclasses
        if piece_type == "King":
            return King(piece_position[0], piece_position[1:], board)
        if piece_type == "Knight":
            return Knight(piece_position[0], piece_position[1:], board)
        if piece_type == "Rook":
            return Rook(piece_position[0], piece_position[1:], board)
        if piece_type == "Bishop":
            return Bishop(piece_position[0], piece_position[1:], board) 
        if piece_type == "Queen":
            return Queen(piece_position[0], piece_position[1:], board)
        
    #--------------- KNIGHT CLASS START ---------------                         ####T_KNIGHT
class Knight(Piece):                        
    def __init__(self, x, y, board: "Board"):
        super().__init__(x, y, "Knight", board)

    def getThreats(self, board: "Board", blocked_pieces = set()) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        all_threats = set()
        if board.checkWithinBoard(self._x-2, self._y-1):
            all_threats.add(CHR(self._x-2) + str(self._y-1))

        if board.checkWithinBoard(self._x-1, self._y-2):
            all_threats.add(CHR(self._x-1) + str(self._y-2))
        
        if board.checkWithinBoard(self._x+2, self._y-1):
            all_threats.add(CHR(self._x+2) + str(self._y-1))

        if board.checkWithinBoard(self._x+1, self._y-2):
            all_threats.add(CHR(self._x+1) + str(self._y-2))

        if board.checkWithinBoard(self._x-1, self._y+2):
            all_threats.add(CHR(self._x-1) + str(self._y+2))

        if board.checkWithinBoard(self._x-2, self._y+1):
            all_threats.add(CHR(self._x-2) + str(self._y+1))

        if board.checkWithinBoard(self._x+1, self._y+2):
            all_threats.add(CHR(self._x+1) + str(self._y+2))

        if board.checkWithinBoard(self._x+2, self._y+1):
            all_threats.add(CHR(self._x+2) + str(self._y+1))
        return all_threats
    #--------------- KNIGHT CLASS END -----------------

    #--------------- KING CLASS START ---------------                         ####T_KING
class King(Piece):
    def __init__(self, x, y, board: "Board"):
        super().__init__(x, y, "King", board)

    def getThreats(self, board: "Board", blocked_pieces = set()) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        all_threats = set()
        if board.checkWithinBoard(self._x-1, self._y-1):
            all_threats.add(CHR(self._x- 1) + str(self._y -1))

        if board.checkWithinBoard(self._x-1, self._y):
            all_threats.add(CHR(self._x - 1) + str(self._y))

        if board.checkWithinBoard(self._x-1, self._y+1):
            all_threats.add(CHR(self._x- 1) + str(self._y+ 1))

        if board.checkWithinBoard(self._x, self._y-1):
            all_threats.add(CHR(self._x) + str(self._y -1))

        if board.checkWithinBoard(self._x, self._y+1):
            all_threats.add(CHR(self._x) + str(self._y + 1))

        if board.checkWithinBoard(self._x+1, self._y-1):
            all_threats.add(CHR(self._x+ 1) + str(self._y -1))

        if board.checkWithinBoard(self._x+1, self._y):
            all_threats.add(CHR(self._x+ 1) + str(self._y))

        if board.checkWithinBoard(self._x+1, self._y+1):
            all_threats.add(CHR(self._x+ 1) + str(self._y +1))
        return all_threats
    #---------------- KING CLASS END -----------------

    #--------------- BISHOP CLASS START ---------------                         ####T_BISHOP
class Bishop(Piece):
    def __init__(self, x, y, board: "Board"):
        super().__init__(x, y, "Bishop", board)

    def getThreats(self, board: "Board", blocked_pieces = set()) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        blocked = board.blocked()
        for piece in blocked_pieces:
            blocked.add(piece.position())
        all_threats = set()
        check_x = self._x - 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x += 1
            check_y += 1
        
        return all_threats
    #--------------- BISHOP CLASS END -----------------

    #--------------- QUEEN CLASS START ---------------                         ####T_QUEEN
class Queen(Piece):
    def __init__(self, x, y, board: "Board"):
        super().__init__(x, y, "Queen", board)


    def getThreats(self, board: "Board", blocked_pieces = set()) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        all_threats = set()
        blocked = board.blocked()
        for piece in blocked_pieces:
            blocked.add(piece.position())
        for i in range(self._y-1, -1, -1):
            all_threats.add(CHR(self._x)+str(i))
            if (CHR(self._x) + str(i)) in blocked:
                break  
        
        for i in range(self._y+1,board.rows()):
            all_threats.add(CHR(self._x)+str(i))
            if (CHR(self._x) + str(i)) in blocked:
                break
                
        for i in range(self._x-1, -1, -1):
            all_threats.add(CHR(i)+str(self._y))
            if (CHR(i) + str(self._y)) in blocked:
                break
                
        for i in range(self._x+1,board.columns()):
            all_threats.add(CHR(i)+str(self._y))
            if (CHR(i) + str(self._y)) in blocked:
                break

        check_x = self._x - 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while board.checkWithinBoard(check_x, check_y):
            all_threats.add(CHR(check_x) + str(check_y))
            if CHR(check_x)+str(check_y) in blocked:
                break
            check_x += 1
            check_y += 1

        return all_threats
    #--------------- QUEEN CLASS END -----------------

    #--------------- ROOK CLASS START ---------------                         ####T_ROOK          
class Rook(Piece):
    def __init__(self, x, y, board: "Board"):
        super().__init__(x, y, "Rook", board)

    def getThreats(self, board: "Board", blocked_pieces = set()) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        all_threats = set()
        blocked = board.blocked()

        for piece in blocked_pieces:
            blocked.add(piece.position())

        for i in range(self._y-1, -1, -1):
            all_threats.add(CHR(self._x)+str(i))
            if (CHR(self._x) + str(i)) in blocked:
                break  
        
        for i in range(self._y+1,board.rows()):
            all_threats.add(CHR(self._x)+str(i))
            if (CHR(self._x) + str(i)) in blocked:
                break
                

        for i in range(self._x-1, -1, -1):
            all_threats.add(CHR(i)+str(self._y))
            if (CHR(i) + str(self._y)) in blocked:
                break

        for i in range(self._x+1,board.columns()):
            all_threats.add(CHR(i)+str(self._y))
            if (CHR(i) + str(self._y)) in blocked:
                break
        
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
    def __init__(self, rows, columns, pieces, obstacles):
        self._ROWS: int = rows              #1-based       
        self._COLUMNS: int = columns        #1-based
        self._MAX_X: int = columns -1       #0-based
        self._MAX_Y: int = rows -1          #0-based
        self._obstacles: list = obstacles   #list of objects subclassed from Piece ## -> List[objects]
        self._pieces = set() #list of strings representing position of each obstacle ## -> List[str]
        self._blocked = set()
        
        for obstacle in obstacles:
            self._blocked.add(obstacle)
        
        for piece in pieces:
            self._pieces.add(Piece.create(piece[0], piece[1], self))
    
    def state(self, remaining_pieces = set()):
        board_state = {}
        for piece in remaining_pieces:
            board_state[piece.x(), int(piece.y())] = piece.type()
        return board_state

    def maxX(self):      #0-based
        return self._MAX_X

    def maxY(self):      #0-based
        return self._MAX_Y
    
    def rows(self):      #1-based
        return self._ROWS

    def columns(self):   #1-based
        return self._COLUMNS

    def pieces(self):
        return self._pieces

    def obstacles(self):
        return self._obstacles
    
    def blocked(self):
        return self._blocked
    
    def checkWithinBoard(self, x: int, y: int) -> bool: #takes in int position values
        return 0 <= x <= self._MAX_X and 0 <= y <= self._MAX_Y
    
    def heuristic(self, remaining_pieces = None):
        if remaining_pieces is None:
            remaining_pieces = self._pieces
        number_of_threatened = 0
        for piece in remaining_pieces:
            for check_threatened in remaining_pieces:
                if check_threatened.position() in piece.threats():
                    number_of_threatened += 1
        return number_of_threatened
    
    def goalTest(self, remaining_pieces = set()) -> bool:
        all_threatened = set()
        for piece in remaining_pieces:
            threatened = piece.getThreats(self, remaining_pieces)
            all_threatened = set.union(all_threatened, threatened)
        
        for piece in remaining_pieces:
            if piece.position() in all_threatened:
                return False
        return True
    

    def getSuccessor(self, piece, remaining_pieces):
        remaining_pieces_new = remaining_pieces.copy()
        remaining_pieces_new.remove(piece)
        return remaining_pieces_new
        
    # def printBoard(self, pieces = None):
    #     if pieces is None:
    #         pieces = self._pieces
    #     all_pieces = {}
    #     for piece in pieces:
    #         all_pieces[piece.position()] = piece.type()[:2].upper()
    #     for obstacle in self._obstacles:
    #         all_pieces[obstacle] = 'OB'
    #     for y in range(self._ROWS):
    #         for x in range(self._COLUMNS):
    #             if CHR(x) + str(y) in all_pieces:
    #                 print(f"{all_pieces[CHR(x) + str(y)]} ", end = '')
    #             else:
    #                 print(" X ", end = '')
    #         print("")
    #     print("-------------------------------")
            
    #--------------- BOARD CLASS END ---------------

##========================== CLASSES END =========================

##========================== FUNCTIONS START ===========================   
def search(rows, columns, pieces, obstacles, k):    #bfs algorithm
    '''The algorithm for local search.'''
    
    board = Board(rows, columns, pieces, obstacles)
    original_pieces = board.pieces()
    # while True:
    for iterations in range(1000):
        pieces = random.sample(original_pieces, k=random.randint(k,len(original_pieces)))
        if board.goalTest(pieces):
            return board.state(pieces)
        while pieces:
            all_successors = []
            current_h = board.heuristic(pieces)
            if len(pieces) > k:
                for i in pieces:
                    successor = board.getSuccessor(i, pieces)
                    successor_h = board.heuristic(successor)
                    if board.goalTest(successor):
                        return board.state(successor)
                    # if(successor_h <= current_h):
                    heapq.heappush(all_successors, (successor_h, successor))
            if all_successors:
                min = []
                min_h, min_pieces = heapq.heappop(all_successors)
                min.append(min_pieces)
                successor_h, successor_pieces = heapq.heappop(all_successors)
                while successor_h == min_h:
                    min.append(successor_pieces)
                    successor_h, successor_pieces = heapq.heappop(all_successors)
                pieces = random.choice(min)
                
            else:
                pieces = None


            

## ******************** !!defining main ************************
def run_local():                                                                        ####T_BFS
    """Definition of main function.

    1. Parsing of file and initialising of environment
    2. Run search()
    """
    # testfile = READ(sys.argv[1])
    testfile = READ("Local7.txt")

    rows = int(next(testfile).split(":")[1])

    columns = int(next(testfile).split(":")[1])

    next(testfile) # burn ## number of obstacles (redundant)
    obstacles = next(testfile).split(":")[1].split()
    if obstacles[0] == "-" : 
        obstacles = []
    set_of_obstacles = set()
    for i in obstacles:
        set_of_obstacles.add(i)
    k = int(next(testfile).split(":")[1])

    next(testfile) # burn ## number of each piece
    next(testfile) # burn ## position header

    pieces = []
    piece = next(testfile)
    while piece:
        pieces.append(piece[1:-1].split(","))        
        piece = next(testfile)
    
    testfile.close()

    return search(rows, columns, pieces, obstacles, k)
## ********************* end of main definition ************************
##============================= FUNCTIONS END =====================================

##======================= MAIN START ============================
t0 = time()
print(run_local())                                  #####T_MAIN
print(time()-t0)
# t0 = time()
# for i in range(1):
#     print(run_local())
# print(time() - t0)