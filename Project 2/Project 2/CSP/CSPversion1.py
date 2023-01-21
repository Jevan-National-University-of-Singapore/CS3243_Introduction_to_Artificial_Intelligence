######################################################################################################
##                         __   __  __           __   __  __   __   __                              ##
##                    |   |  | |   |__| |       |__  |__ |__| |__| |   |__|                         ##
##                    |__ |__| |__ |  | |__      __| |__ |  | |  \ |__ |  |                         ##
##                                                                                                  ##
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
##          . state()                                                                               ##
##          . goalTest()                                                                            ##
##          . getSuccessor(i)                                                                       ##
##          . heuristic()                                                                           ##
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

##=================== GLOBAL FUNCTIONS START ==================             ####T_GBL
import sys
import copy

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
    def __init__(self, rows, columns, enemy_pieces, obstacles, threats = set()):
        self._ROWS: int = rows              #1-based       
        self._COLUMNS: int = columns        #1-based
        self._MAX_X: int = columns -1       #0-based
        self._MAX_Y: int = rows -1          #0-based
        self._blocked: set = obstacles   #list of objects subclassed from Piece ## -> List[objects]
        self._enemy_pieces: list = enemy_pieces #list of strings representing position of each obstacle ## -> List[str]
        self._threats = threats
        self._invalid_positions = obstacles

        for enemy in enemy_pieces:
            self._blocked.add(enemy.position())
            self._invalid_positions.add(enemy.position())
    
    def __copy__(self):
        cls = self.__class__
        board_copy = cls.__new__(cls)
        board_copy.__dict__["_ROWS"] = self.__dict__["_ROWS"]
        board_copy.__dict__["_COLUMNS"] = self.__dict__["_COLUMNS"]
        board_copy.__dict__["_MAX_X"] = self.__dict__["_MAX_X"]
        board_copy.__dict__["_MAX_Y"] = self.__dict__["_MAX_Y"]
        board_copy.__dict__["_blocked"] = self.__dict__["_blocked"].copy()
        board_copy.__dict__["_enemy_pieces"] = self.__dict__["_enemy_pieces"].copy()
        board_copy.__dict__["_threats"] = self.__dict__["_threats"].copy()
        board_copy.__dict__["_invalid_positions"] = self.__dict__["_invalid_positions"].copy()
        return board_copy 
    

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
    
    def invalidPositions(self):
        return self._invalid_positions
    
    def checkWithinBoard(self, x: int, y: int) -> bool: #takes in int position values
        return 0 <= x <= self._MAX_X and 0 <= y <= self._MAX_Y

    def getAllThreats(self) -> set:
        threatened = set()
        for piece in self._enemy_pieces:
            threatened = piece.getThreats(threatened, self)
        return threatened
    
    def addPiece(self, added_piece) -> bool:
        self._enemy_pieces.append(added_piece)
        self._blocked.add(added_piece.position())
        self._threats = added_piece.getThreats(self._threats, self)
        self._invalid_positions = set.union(self._threats, self._blocked)
        # print(f"{added_piece.position()}  {self._threats}")
        for piece in self._enemy_pieces:
            if piece.position() in self._threats:
                return False
        return True

        
    
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

    def state(self):
        board_state = {}
        for piece in self._enemy_pieces:
            board_state[piece.x(), int(piece.y())] = piece.type()
        return board_state
        
    # def printBoard(self):
    #     for y in range(self._ROWS):
    #         for x in range(self._COLUMNS):
    #             position = CHR(x) + str(y)
    #             if position in self._pieces:
    #                 print(f"{self._pieces[CHR(x) + str(y)].type().upper()[0:2]} ", end = '')
    #             elif position in self._obstacles:
    #                 print(f"OB ", end = '')
    #             else:
    #                 print(" X ", end = '')
    #         print("")
    #     print("-------------------------------")
            
    #--------------- BOARD CLASS END ---------------

##========================== CLASSES END =========================

                        

##========================== FUNCTIONS START ===========================   
def search(rows, columns, pieces, obstacles):    #Hill climbing algorithm
    '''The algorithm for local search.'''
    start = Board(rows, columns, [], obstacles)
    stack = [(pieces, start)]         #frontier
    # visited_nodes = {start: Node(position=start, previous=None)}

    # if start in threatened:
    #     return [], 1 #no solution
    # elif start in goals: #check start is goal
    #     move = [(start[0], start_y_int)]
    #     return [move], 1
    #start is not goal
    counter = 100
    while stack and counter:              
        # print(stack)                              #algo start
        current_pieces_left, current_state = stack.pop()     #get a frontier node
        invalid_positions = current_state.invalidPositions()
        for x in range(columns):
            for y in range(rows):
                assignment = None
                if current_pieces_left["Queen"] > 0:
                    assignment = "Queen"
                elif current_pieces_left["Rook"] > 0:
                    assignment = "Rook"
                elif current_pieces_left["Bishop"] > 0:
                    assignment = "Bishop"
                elif current_pieces_left["Knight"] > 0:
                    assignment = "Knight"
                else:
                    assignment = "King"                                                                         
                
                position = CHR(x)+str(y)
                if position not in invalid_positions:
                    successor = copy.copy(current_state)
                    if successor.addPiece(Piece.create(assignment, position)):
                        if current_pieces_left["Total"] == 1:
                            return successor.state()
                        successor_current_pieces_left = current_pieces_left.copy()
                        successor_current_pieces_left[assignment] -= 1
                        successor_current_pieces_left["Total"] -= 1
                        stack.append((successor_current_pieces_left, successor))

        # for next_position in board.getLegalMovesPositions(current_x_int, current_y_int):    #get all legal moves i.e. within board
        #     if next_position not in visited_nodes:                                          #check not visited then continue
        #         visited_nodes[next_position] = Node(position=next_position, previous=current_position)        #add to visited on pop
        #         if next_position not in threatened and next_position not in blocked:        #if valid then add to frontier
        #             stack.append(next_position)
        #             if next_position in goals:      #goal test
        #                 return visited_nodes[next_position].getPath(visited_nodes), len(visited_nodes)
        counter -= 1

    # return [],len(visited_nodes)
    




            

## ******************** !!defining main ************************
def run_CSP():                                                                        ####T_LOCAL
    """Definition of main function.

    1. Parsing of file and initialising of environment
    2. Run search()
    """
    testfile = READ(sys.argv[1])
    # testfile = READ("CSP10.txt")

    rows = int(next(testfile).split(":")[1])

    columns = int(next(testfile).split(":")[1])

    next(testfile) # burn ## number of obstacles (redundant)
    obstacles = next(testfile).split(":")[1].split()
    obstacles = set() if obstacles[0] == "-" else set(obstacles)
        

    pieces = next(testfile).split(":")[1].split()

    pieces_dict = {"Total": sum(int(piece) for piece in pieces), "King": int(pieces[0]), "Queen":int(pieces[1]), "Bishop":int(pieces[2]), "Rook":int(pieces[3]), "Knight":int(pieces[4])}
    
    testfile.close()


    return search(rows, columns, pieces_dict, obstacles)
## ********************* end of main definition ************************
##============================= FUNCTIONS END =====================================

##======================= MAIN START ============================
# t0 = time()
# print(run_CSP())                                          #####T_MAIN
# print(time() - t0)