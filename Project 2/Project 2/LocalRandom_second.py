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
#LocalGreedyWithSide_h2

##=================== GLOBAL FUNCTIONS START ==================             ####T_GBL
import sys
import random
import heapq
# from time import time


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
    def __init__(self, x: str, y: str, pieceType: str):
        self._PIECE_TYPE = pieceType
        self._x = INT(x)
        self._y = int(y)
        self._position = x+y
    
    def x(self) -> str:
        return CHR(self._x)
    
    def y(self) -> str:
        return str(self._y)

    def type(self):
        return self._PIECE_TYPE
    
    def position(self) -> str:
        return self._position

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

            *Include blocked positions
        """
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
    def __init__(self, x, y):
        super().__init__(x, y, "King")

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
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
    def __init__(self, x, y):
        super().__init__(x, y, "Bishop")

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        blocked = board.blocked()
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
    def __init__(self, x, y):
        super().__init__(x, y, "Queen")


    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        blocked = board.blocked()
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
    def __init__(self, x, y):
        super().__init__(x, y, "Rook")

    def getThreats(self, all_threats: set, board: "Board") -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Include blocked positions
        """
        blocked = board.blocked()
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
        self._pieces: list = pieces #list of strings representing position of each obstacle ## -> List[str]
        self._blocked = set()
        
        for obstacle in obstacles:
            self._blocked.add(obstacle)
        
        for piece in pieces:
            self._blocked.add(piece.position())

        self._heuristic: int = self.calculateHeuristic()
    
    def __lt__(self, board): #comparator
        return self._heuristic <= board.heuristic()

    def state(self):
        board_state = {}
        for piece in self._pieces:
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

    def getAllThreats(self) -> set:
        threatened = set()
        for piece in self._pieces:
            threatened = piece.getThreats(threatened, self)        
        return threatened
    
    def calculateHeuristic(self) -> int:
        number_of_threatened = 0
        for piece in self._pieces:
            threatened = piece.getThreats(set(), self)
            for check_threatened in self._pieces:
                if check_threatened.position() in threatened:
                    number_of_threatened += 1
        return number_of_threatened
    
    def heuristic(self):
        return self._heuristic
    
    def goalTest(self) -> bool:
        return self.heuristic() == 0

    def getSuccessor(self, i):
        new_pieces = self._pieces.copy()
        new_pieces.pop(i)
        return Board(self._ROWS, self._COLUMNS, new_pieces, self._obstacles)
        
    # def printBoard(self):
    #     all_pieces = {}
    #     for piece in self._pieces:
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
    # for iteration in range(50):
    while True:
    # random.seed(100)
    # random.seed(500)
    # for iterations in range(100):
        # print(iterations)
        # number_of_pieces_taken_away = 0.5*(len(pieces)-k)/k
        # number_of_pieces = round(len(pieces)- number_of_pieces_taken_away)
        # board = Board(rows, columns, random.sample(pieces, number_of_pieces), obstacles)
        board = Board(rows, columns, random.sample(pieces, k=random.randint(k,len(pieces))), obstacles)
        # board = Board(rows, columns, random.sample(pieces, k=random.randint(k,  round(   len(pieces) -   0.5*(    (len(pieces)-k))/k   ))), obstacles)
        if board.goalTest():
            # board.printBoard()
            return board.state()
        while board:
            lower_successors = []
            equal_successors = []
            all_successors = []
            current_h = board.heuristic()
            number_of_pieces = len(board.pieces())
            goal_current_ratio = k/number_of_pieces
            if number_of_pieces > k:
                # random.sample(range(10, 30), 5)
                for i in range(number_of_pieces):
                    if random.random() < goal_current_ratio:              ###>0.01: 197.473          ##>0.1: 128.39            #<k/len(pieces): 59.34s  ###queen: 159.16 max, total 1856
                        successor = board.getSuccessor(i)
                        if(successor.heuristic() < current_h):
                            if successor.goalTest():
                                # successor.printBoard()
                                return successor.state()
                            lower_successors.append(successor)
                        elif(successor.heuristic() == current_h):
                            if successor.goalTest():
                                # successor.printBoard()
                                return successor.state()
                            equal_successors.append(successor)
                        elif random.random() < goal_current_ratio:       ###< k/len:49.86
                            all_successors.append(successor)

            board = None
            # if all_successors and random.random() > 0.9:        ####0.95 = 338s     ####0.9 = 335s
            #     board = random.choice(all_successors)
            if lower_successors:
                heapq.heapify(lower_successors)
                board = heapq.heappop(lower_successors)
            elif equal_successors:
                board = equal_successors[0]
            elif all_successors and random.random() > 0.5:
                board = all_successors[0]




            

## ******************** !!defining main ************************
def run_local():                                                                        ####T_BFS
    """Definition of main function.

    1. Parsing of file and initialising of environment
    2. Run search()
    """
    testfile = READ(sys.argv[1])
    # testfile = READ("allqueen.txt")

    rows = int(next(testfile).split(":")[1])

    columns = int(next(testfile).split(":")[1])

    next(testfile) # burn ## number of obstacles (redundant)
    obstacles = next(testfile).split(":")[1].split()
    if obstacles[0] == "-" : 
        obstacles = []

    k = int(next(testfile).split(":")[1])

    next(testfile) # burn ## number of each piece
    next(testfile) # burn ## position header

    pieces = []
    piece = next(testfile)
    while piece:
        piece_type, piece_position = piece[1:-1].split(",")
        pieces.append(Piece.create(piece_type, piece_position))
        piece = next(testfile)
    
    testfile.close()


    return search(rows, columns, pieces, obstacles, k)
## ********************* end of main definition ************************
##============================= FUNCTIONS END =====================================

##======================= MAIN START ============================
# t0 = time()
# print(run_local())                                          #####T_MAIN
# print(time() - t0)