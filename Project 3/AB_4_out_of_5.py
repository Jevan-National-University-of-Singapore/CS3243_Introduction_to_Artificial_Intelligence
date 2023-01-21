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
import copy
KNIGHT_THREATS = {
    (0, 0): {(1, 2), (2,1)},                            (1, 0): {(3,1),(2,2),(0,2)},                       (2, 0): {(0,1), (1,2), (3,2),(4,1)},                                      (3, 0): {(1,1),(2,2),(4,2)},                                  (4, 0): {(3,2),(2,1)},
    (0, 1): {(2, 0), (1, 3), (2, 2)},                   (1, 1): {(3,0),(3,2),(2,3),(0,3)},                 (2, 1): {(0,2), (1,3), (3,3),(4,2),(0,0),(4,0)},                          (3, 1): {(1,0),(1,2),(2,3),(4,3)},                            (4, 1): {(2,0),(3,3),(2,2)},
    (0, 2): {(1, 0), (2, 1), (1, 4), (2, 3)},           (1, 2): {(0,0),(2,0),(3,1),(3,3),(2,4),(0,4)},     (2, 2): {(0,3), (1,4), (3,4),(4,3),(0,1),(4,1), (1,0), (3,0)},            (3, 2): {(4,0), (2,0), (1,1), (1,3), (2,4), (4,4)},           (4, 2): {(3,0),(2,1),(3,4),(2,3)},
    (0, 3): {(1, 1), (2,2), (2, 4)},                    (1, 3): {(0,1),(2,1),(3,2),(3,4)},                 (2, 3): {(0,2), (1,1), (3,1),(4,2),(0,4),(4,4)},                          (3, 3): {(4,1), (2,1), (1,2), (1,4)},                         (4, 3): {(3,1),(2,2),(2,4)},
    (0, 4): {(1, 2), (2, 3)},                           (1, 4): {(0,2),(2,2),(3,3)},                       (2, 4): {(0,3), (1,2), (3,2),(4,3)},                                      (3, 4): {(4,2), (2,2), (1,3)},                                (4, 4): {(3,2),(2,3)}
}

KING_THREATS = {
    (0, 0): {(0, 1), (1,0), (1,1)},                            (1, 0): {(0,0),(0,1),(1,1), (2,1), (2,0)},                             (2, 0): {(1,0), (1,1), (2,1),(3,1), (3,0)},                            (3, 0): {(4,0),(4,1),  (3,1), (2,1), (2,0)},                            (4, 0): {(4, 1), (3,0), (3,1)},                  
    (0, 1): {(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)},          (1, 1): {(0,0), (1,0), (2,0),(0,1),(0,2),(1,2), (2,2), (2,1)},         (2, 1): {(1,1), (1,2), (2,2),(3,2), (3,1), (1,0),(2,0),(3,0)},         (3, 1): {(4,0), (3,0), (2,0),(4,1),(4,2),(2,2), (2,2), (2,1)},          (4, 1): {(4, 0), (3, 0), (3, 1), (3, 2), (4, 2)},
    (0, 2): {(0, 1), (1, 1), (1, 2), (1, 3), (0, 3)},          (1, 2): {(0,1), (1,1), (2,1),(0,2),(0,3),(1,3), (2,3), (2,2)},         (2, 2): {(1,2), (1,3), (2,3),(3,3), (3,2), (1,1),(2,1),(3,1)},         (3, 2): {(4,1), (3,1), (2,1),(4,2),(4,3),(2,3), (2,3), (2,2)},          (4, 2): {(4, 1), (3, 1), (3, 2), (3, 3), (4, 3)},
    (0, 3): {(0, 4), (1, 4), (1, 3), (1, 2), (0, 2)},          (1, 3): {(0,2), (1,2), (2,2),(0,3),(0,4),(1,4), (2,4), (2,3)},         (2, 3): {(1,3), (1,4), (2,4),(3,4), (3,3), (1,2),(2,2),(3,2)},         (3, 3): {(4,2), (3,2), (2,2),(4,3),(4,4),(2,4), (2,4), (2,3)},          (4, 3): {(4, 4), (3, 4), (3, 3), (3, 2), (4, 2)},
    (0, 4): {(0, 3), (1,4), (1,3)},                            (1, 4): {(0,4),(0,3),(1,3), (2,3), (2,4)},                             (2, 4): {(1,4), (1,3), (2,3),(3,3), (3,4)},                            (3, 4): {(4,4),(4,3),  (3,3), (2,3), (2,4)},                            (4, 4): {(4, 3), (3,4), (3,3)},                  
}
def INT(character: str) -> int: ##converts alpabets to integers
    return ord(character)-97

def CHR(integer: int) -> str: ##converts integers to alphabets
    return chr(integer+97)

# def CHR_PARSE(integer: int) -> str: ##converts integers to alphabets
#     return chr(integer+97)


def checkWithinBoard(x, y):
    return 0 <= x <= 4 and 0 <= y<=4
##==================== GLOBAL FUNCTIONS END ====================
##========================= CLASSES START ======================================= ####T_CLASS
class Piece:                      # base class                                  ####T_PIECE
    def __init__(self, x: int, y: int, pieceType: str, team: str, heuristic: float):
        self._PIECE_TYPE = pieceType
        self._x = x
        self._y = y
        self._team = team
        self.heuristic = heuristic
    
    def x(self) -> int:
        return self._x
    
    def y(self) -> int:
        return self._y

    def type(self):
        return self._PIECE_TYPE

    def moveTo(self, position):
        self._x, self._y = position
    
    def team(self):
        return self._team

    @staticmethod
    def create(piece_type, piece_x, piece_y, team) -> object:  #create corresponding Piece subclasses
        if piece_type == "King":
            return King(piece_x, piece_y, team)
        elif piece_type == "Knight":
            return Knight(piece_x, piece_y, team)
        elif piece_type == "Rook":
            return Rook(piece_x, piece_y, team)
        elif piece_type == "Bishop":
            return Bishop(piece_x, piece_y, team) 
        elif piece_type == "Queen":
            return Queen(piece_x, piece_y, team)
        else:
            return Pawn(piece_x, piece_y, team)
        
    #--------------- KNIGHT CLASS START ---------------                         ####T_KNIGHT
class Knight(Piece):                        
    def __init__(self, x, y, team):
        super().__init__(x, y, "Knight", team, 3)

    def getMoves(self, my_pieces, enemy_pieces):
        all_moves = self.getThreats(my_pieces, enemy_pieces)
        next_move = next(all_moves)
        while next_move:
            if next_move not in my_pieces:
                yield next_move
            next_move = next(all_moves)
        yield None

        # for move in KNIGHT_THREATS[(self._x, self._y)]:
        #     if move not in my_pieces:
        #         yield move
        # yield None

    def getThreats(self, my_team, enemy_team) -> set:
        if checkWithinBoard(self._x-2, self._y-1):
            yield (self._x-2, self._y-1)

        if checkWithinBoard(self._x-1, self._y-2):
            yield (self._x-1, self._y-2)
        
        if checkWithinBoard(self._x+2, self._y-1):
            yield (self._x+2, self._y-1)

        if checkWithinBoard(self._x+1, self._y-2):
            yield (self._x+1, self._y-2)

        if checkWithinBoard(self._x-1, self._y+2):
            yield (self._x-1, self._y+2)

        if checkWithinBoard(self._x-2, self._y+1):
            yield (self._x-2, self._y+1)

        if checkWithinBoard(self._x+1, self._y+2):
            yield (self._x+1, self._y+2)

        if checkWithinBoard(self._x+2, self._y+1):
            yield (self._x+2, self._y+1)
        yield None


    #--------------- KNIGHT CLASS END -----------------

    #--------------- KING CLASS START ---------------                         ####T_KING
class King(Piece):
    def __init__(self, x, y, team):
        self._team = team
        super().__init__(x, y, "King", team, 10000) ## high enough heuristic such that without this piece, impossible to get best_value
    
    def getMoves(self, my_pieces, enemy_pieces):
        all_moves = self.getThreats(my_pieces, enemy_pieces)
        next_move = next(all_moves)
        while next_move:
            if next_move not in my_pieces:
                yield next_move
            next_move = next(all_moves)
        yield None
        # for move in KING_THREATS[(self._x, self._y)]:
        #     if move not in my_pieces:
        #         yield move
        # yield None
    

    def getThreats(self, my_team, enemy_team) -> set:
        if checkWithinBoard(self._x-1, self._y-1):
            yield (self._x- 1, self._y -1)

        if checkWithinBoard(self._x-1, self._y):
            yield (self._x - 1, self._y)

        if checkWithinBoard(self._x-1, self._y+1):
            yield (self._x- 1, self._y+ 1)

        if checkWithinBoard(self._x, self._y-1):
            yield (self._x, self._y -1)

        if checkWithinBoard(self._x, self._y+1):
            yield (self._x, self._y + 1)

        if checkWithinBoard(self._x+1, self._y-1):
            yield (self._x+ 1, self._y -1)

        if checkWithinBoard(self._x+1, self._y):
            yield (self._x+ 1, self._y)

        if checkWithinBoard(self._x+1, self._y+1):
            yield (self._x+ 1, self._y +1)
        yield None
    
    #---------------- KING CLASS END -----------------

    #--------------- BISHOP CLASS START ---------------                         ####T_BISHOP
class Bishop(Piece):
    def __init__(self, x, y, team):
        super().__init__(x, y, "Bishop", team, 3) # heuristic = 4.16 average moves for each position on the board

    def getMoves(self, my_pieces, enemy_pieces):
        all_moves = self.getThreats(my_pieces, enemy_pieces)
        next_move = next(all_moves)
        while next_move:
            yield next_move
            next_move = next(all_moves)
        yield None

    def getThreats(self, my_team, enemy_team) -> set:
        check_x = self._x - 1
        check_y = self._y - 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x += 1
            check_y += 1
        
        yield None
    #--------------- BISHOP CLASS END -----------------

    #--------------- QUEEN CLASS START ---------------                         ####T_QUEEN
class Queen(Piece):
    def __init__(self, x, y, team):
        super().__init__(x, y, "Queen", team, 9)#12.16)

    def getMoves(self, my_pieces, enemy_pieces):
        all_moves = self.getThreats(my_pieces, enemy_pieces)
        next_move = next(all_moves)
        while next_move:
            yield next_move
            next_move = next(all_moves)
        yield None

    def getThreats(self, my_team, enemy_team) -> set:
        """Adds all threatened positions to the set of threatened positions on the board.

            *Does not include blocked positions
        """
        for i in range(self._y-1, -1, -1):
            new_position = (self._x, i)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
                
        
        for i in range(self._y+1,5):
            new_position = (self._x, i)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break

        for i in range(self._x-1, -1, -1):
            new_position = (i, self._y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break

        for i in range(self._x+1,5):
            new_position = (i, self._y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break   

        check_x = self._x - 1
        check_y = self._y - 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x -= 1
            check_y -= 1

        check_x = self._x - 1
        check_y = self._y + 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x -= 1
            check_y += 1

        check_x = self._x + 1
        check_y = self._y - 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x += 1
            check_y -= 1

        check_x = self._x + 1
        check_y = self._y + 1
        while checkWithinBoard(check_x, check_y):
            new_position = (check_x, check_y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
            check_x += 1
            check_y += 1
        
        yield None
    #--------------- QUEEN CLASS END -----------------

    #--------------- ROOK CLASS START ---------------                         ####T_ROOK          
class Rook(Piece):
    def __init__(self, x, y, team):
        super().__init__(x, y, "Rook", team, 5)

    def getMoves(self, my_pieces, enemy_pieces):
        all_moves = self.getThreats(my_pieces, enemy_pieces)
        next_move = next(all_moves)
        while next_move:
            yield next_move
            next_move = next(all_moves)
        yield None

    def getThreats(self, my_team, enemy_team) -> set:

        for i in range(self._y-1, -1, -1):
            new_position = (self._x, i)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break
                
        
        for i in range(self._y+1,5):
            new_position = (self._x, i)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break

        for i in range(self._x-1, -1, -1):
            new_position = (i, self._y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break


        for i in range(self._x+1,5):
            new_position = (i, self._y)
            if new_position in my_team:
                break
            yield new_position
            if new_position in enemy_team:
                break                
        
        yield None
    #--------------- KNIGHT CLASS END -----------------
class Pawn(Piece):
    def __init__(self, x, y, team):
        self._y_limit = 4 if team == "White" else 0
        self._y_movement = 1 if team == "White" else -1
        super().__init__(x, y, "Pawn", team, 1)
    def getThreats(self, my_team, enemy_team) -> set:
        if self._y == self._y_limit:
            yield None
        if self._x != 0:
            yield (self._x - 1, self._y + self._y_movement)
        if self._x != 4:
            yield (self._x + 1, self._y + self._y_movement)
        yield None
    
    def getMoves(self, my_team, enemy_team):
        if self._y != self._y_limit:
            move_position = (self._x, self._y+self._y_movement)
            if move_position not in enemy_team and move_position not in my_team:
                yield move_position
            if self._x != 0:
                move_position = (self._x - 1, self._y + self._y_movement)
                if move_position in enemy_team:
                    yield move_position
            if self._x != 4:
                move_position = (self._x + 1, self._y + self._y_movement)
                if move_position in enemy_team:
                    yield move_position
        yield None


    #--------------- BOARD CLASS START ---------------              ####T_BOARD
class Board:
    def __init__(self, my_pieces, enemy_pieces):
        self._ROWS: int = 5             #1-based       
        self._COLUMNS: int = 5        #1-based
        self._MAX_X: int = 4       #0-based
        self._MAX_Y: int = 4          #0-based
        self._my_pieces = my_pieces
        self._enemy_pieces: list = enemy_pieces #list of strings representing position of each obstacle ## -> List[str]


    def maxX(self):      #0-based
        return self._MAX_X

    def maxY(self):      #0-based
        return self._MAX_Y
    
    def rows(self):      #1-based
        return self._ROWS

    def columns(self):   #1-based
        return self._COLUMNS
    
    def pieces(self):
        return self._my_pieces

    def enemies(self):
        return self._enemy_pieces

    @staticmethod
    def getAllThreats(my_pieces, enemy_pieces) -> set:
        all_threats = set()
        for pos, piece in my_pieces.items():
            all_current_threats = piece.getThreats(my_pieces, enemy_pieces)
            threat = next(all_current_threats)
            while threat:
                all_threats.add(threat)
                threat = next(all_current_threats)

        return all_threats

    @staticmethod
    def makeMove(pieces, current_state, next_state):
        piece_copy = copy.copy(pieces[current_state])
        piece_copy.moveTo(next_state)
        pieces_copy = pieces.copy()
        pieces_copy.pop(current_state)
        pieces_copy[next_state] = piece_copy
        return pieces


    # @staticmethod
    # def printBoard(white_pieces, black_pieces):
    #     for y in range(5):
    #         for x in range(5):
    #             if (x, y) in white_pieces:
    #                 piece = white_pieces[(x, y)]
    #                 print(f"{piece.type()[0:2].upper()} ", end="")
    #             elif (x, y) in black_pieces:
    #                 piece = black_pieces[(x, y)]
    #                 print(f"{piece.type()[0:2].upper()} ", end="")
    #             else:
    #                 print (" X ", end="")
    #         print("")
    #     print("===========================")
    
    @staticmethod
    def getAllValidSuccessors(white_pieces, black_pieces, white_turn, heuristic):
        if white_turn:
            for position, piece in white_pieces.items():
                all_moves_of_piece = piece.getMoves(white_pieces, black_pieces)
                current_move = next(all_moves_of_piece)
                while current_move:
                    new_heuristic = heuristic
                    new_black_pieces = black_pieces
                    if current_move in black_pieces:
                        new_black_pieces = black_pieces.copy()
                        new_heuristic = heuristic
                        new_black_pieces.pop(current_move)
                    new_white_pieces = Board.makeMove(white_pieces, position, current_move)
                    yield new_white_pieces, new_black_pieces, new_heuristic
                    current_move = next(all_moves_of_piece)
        else:
            for position, piece in black_pieces.items():
                all_moves_of_piece = piece.getMoves(black_pieces, white_pieces)
                current_move = next(all_moves_of_piece)
                while current_move:
                    new_heuristic = heuristic
                    new_white_pieces = white_pieces
                    if current_move in white_pieces:
                        new_white_pieces = white_pieces.copy()
                        new_heuristic -= white_pieces[current_move].heuristic
                        new_white_pieces.pop(current_move)
                    new_black_pieces = Board.makeMove(black_pieces, position, current_move)
                    yield new_white_pieces, new_black_pieces, new_heuristic
                    current_move = next(all_moves_of_piece)
        yield None
    
    def getAllInitialValidSuccessors(white_pieces, black_pieces, heuristic):
        for position, piece in white_pieces.items():
            all_moves_of_piece = piece.getMoves(white_pieces, black_pieces)
            current_move = next(all_moves_of_piece)
            while current_move:
                new_black_pieces = black_pieces
                new_heuristic = heuristic
                if current_move in black_pieces:
                    new_black_pieces = black_pieces.copy()
                    new_heuristic += black_pieces[current_move].heuristic
                    new_black_pieces.pop(current_move)
                new_white_pieces = Board.makeMove(white_pieces, position, current_move)
                yield new_white_pieces, new_black_pieces, new_heuristic, ((piece.x(), piece.y()),current_move)
                current_move = next(all_moves_of_piece)
        yield None

    @staticmethod
    def heuristic(my_pieces, enemy_pieces):
        points = 0
        for position, my_piece in my_pieces.items():
            if my_piece.type() == "King":
                all_threats = Board.getAllThreats(my_pieces, enemy_pieces)
                if (position) in all_threats:
                    points -= 400
            points += my_piece.heuristic
        for position, enemy_piece in enemy_pieces.items():
            points -= enemy_piece.heuristic
        return 1**points
        
    # def heuristic(my_pieces, enemy_pieces):
    #     points = 0
    #     for position, my_piece in my_pieces.items():
    #         points += my_piece.heuristic
    #     for position, enemy_piece in enemy_pieces.items():
    #         points -= enemy_piece.heuristic
    #     return points

    
    #--------------- BOARD CLASS END ---------------


##========================== FUNCTIONS START ===========================   

def bestMove(move):
    current_state, transition_state = move
    return (CHR(current_state[0]), current_state[1]), (CHR(transition_state[0]),transition_state[1])

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(node, depth, is_max, alpha, beta):
    white_pieces, black_pieces, heuristic, move = node
    if depth == 2:
        return move, heuristic
    all_valid_successors = Board.getAllValidSuccessors(white_pieces, black_pieces, is_max, heuristic)
    successor = next(all_valid_successors)
    if successor is None:
        return move, 0
    if is_max:
        highest_value = -10000000
        best_move = move
        while successor and beta <= alpha:
            successor_node = successor + (move,)
            new_move, value = ab(successor_node, depth+1, False, alpha, beta)
            if value > highest_value:
                highest_value = value
                best_move = new_move 
            alpha = max(alpha, highest_value)
            successor=next(all_valid_successors)
        return best_move, highest_value
    else:
        lowest_value = 10000000
        best_move = move
        while successor and beta <= alpha:
            successor_node = successor + (move,)
            new_move, value = ab(successor_node, depth+1, True, alpha, beta)
            if value < lowest_value:
                lowest_value = value
                best_move = new_move
            beta = min(beta, lowest_value)
            successor = next(all_valid_successors)
        return best_move, lowest_value



    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    pieces = {}
    enemy_pieces = {}

    for piece in gameboard.items():
        position = piece[0]
        metadata = piece[1]
        team = metadata[1]
        x = INT(position[0])
        y = int(position[1])
        if team == "White":
            pieces[(x, y)] = Piece.create(metadata[0], x, y, "White")
        else:
            enemy_pieces[(x, y)] = Piece.create(metadata[0], x, y, "Black")

    # Board.printBoard(pieces, enemy_pieces)
    all_valid_successors = Board.getAllInitialValidSuccessors(pieces, enemy_pieces, Board.heuristic(pieces, enemy_pieces))
    successor = next(all_valid_successors)
    highest_value = -100
    best_move = None
    alpha = 0
    beta = 0

    while successor and beta <= alpha:
        new_move, value = ab(successor, 0, False, alpha, beta)
        if value > highest_value:
            highest_value = value
            best_move = new_move 
        alpha = max(alpha, highest_value)
        successor = next(all_valid_successors)

    return bestMove(best_move)


    

# starting = {('a', 1): ('Pawn', 'White'), ('a', 3): ('Pawn', 'Black'), ('b', 1): ('Pawn', 'White'), ('b', 3): ('Pawn', 'Black'), ('c', 1): ('Pawn', 'White'), ('c', 3): ('Pawn', 'Black'),
# ('d', 1): ('Pawn', 'White'), ('d', 3): ('Pawn', 'Black'), ('e', 1): ('Pawn', 'White'), ('e', 3): ('Pawn', 'Black'), ('a', 0): ('Rook', 'White'), ('a', 4): ('Rook', 'Black'),
# ('b', 0): ('Knight', 'White'), ('b', 4): ('Knight', 'Black'), ('c', 0): ('Bishop', 'White'), ('c', 4): ('Bishop', 'Black'), ('d', 0): ('Queen', 'White'), ('d', 4): ('Queen', 'Black'), 
# ('e', 0): ('King', 'White'), ('e', 4): ('King', 'Black')}


# move = studentAgent(starting)
# print(move)

# previous, next_move = move
# starting[next_move]=starting[previous]

# for i in starting:
#     if starting[i][1] == "Black":
#         starting[i] = (starting[i][0], "White")
#     else:
#         starting[i] = (starting[i][0], "Black")

# starting.pop(previous)
# move = studentAgent(starting)
# print(move)

# previous, next_move = move
# starting[next_move]=starting[previous]

# for i in starting:
#     if starting[i][1] == "Black":
#         starting[i] = (starting[i][0], "White")
#     else:
#         starting[i] = (starting[i][0], "Black")

# starting.pop(previous)
# move = studentAgent(starting)
# print(move)

# previous, next_move = move
# starting[next_move]=starting[previous]