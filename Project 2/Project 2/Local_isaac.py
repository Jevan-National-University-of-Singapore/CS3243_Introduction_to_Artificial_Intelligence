from pickle import FALSE
import sys
import copy
import heapq
import random
from time import time
### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
def alphaToNum(char):
    return ord(char) - 97

def numToAlpha(int):
    return chr(int + 97)
class Piece:
    def __init__(self, t, row, column, prev=None):
        self.type = t
        self.row = row
        self.column = column
        self.prev = prev
    
    def __repr__(self):
        return "<%s, %s, (%s, %s)>" % (self.type, self.cost, self.row, self.column)

    def getRow(self):
        return self.row

    def getCol(self):
        return self.column

class Knight(Piece):
    def __init__(self, row, column):
        super().__init__('Knight', row, column, None)
    
    #blocks out positions where the enemy can threaten my piece and also block out the piece that it is currently on
    def putThreats(self, board):
        threats = board.getThreats()
        blocked = board.getBlocked()
        assignedThreats = board.getAssignedThreats()
        enemies = board.getEnemy()
        maxRow = board.getMaxRow()
        maxCol = board.getMaxCol()
        knight_movements = [[-1, -2], [-2, -1], [-2, 1], [-1, 2], [1, -2], [2, -1], [2, 1], [1, 2]]
        temp = []
        for i in range(8):
            new_row = self.getRow() + knight_movements[i][0]
            new_col = self.getCol() + knight_movements[i][1]
            if (0 <= new_row < maxRow) and (0  <= new_col < maxCol):
                temp.append((new_row, new_col))
                threats.append((new_row, new_col))
                #print(new_row, new_col)
        row = self.getRow()
        col = self.getCol()
        # if (row, col) not in blocked:
        #     blocked.append((row, col))
        #temp.remove((row, col))
        temp = list(filter((row, col).__ne__, temp))
        assignedThreats[(row, col)] = temp
        enemies[(row, col)] = 'Knight'


class King(Piece):
    def __init__(self, row, column):
        super().__init__('King', row, column, None)
    
    #blocks out positions where the enemy can threaten my piece and also block out the piece that it is currently on
    def putThreats(self, board):
        threats = board.getThreats()
        blocked = board.getBlocked()
        assignedThreats = board.getAssignedThreats()
        enemies = board.getEnemy()
        maxRow = board.getMaxRow()
        maxCol = board.getMaxCol()
        temp = []
        kings_movements = [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for i in range(8):
            new_row = self.getRow() + kings_movements[i][0]
            new_col = self.getCol() + kings_movements[i][1]
            if (0 <= new_row < maxRow) and (0  <= new_col < maxCol):
                temp.append((new_row, new_col))
                threats.append((new_row, new_col))
                #print(new_row, new_col)
        row = self.getRow()
        col = self.getCol()
        # if (row, col) not in blocked:
        #     blocked.append((row, col))
        #temp.remove((row, col))
        temp = list(filter((row, col).__ne__, temp))
        assignedThreats[(row, col)] = temp
        enemies[(row, col)] = 'King'
    
class Bishop(Piece):
    def __init__(self, row, column):
        super().__init__('Bishop', row, column, None)

    #blocks out positions where the enemy can threaten my piece and also block out the piece that it is currently on
    def putThreats(self, board):
        threats = board.getThreats()
        blocked = board.getBlocked()
        assignedThreats = board.getAssignedThreats()
        enemies = board.getEnemy()
        maxRow = board.getMaxRow()
        maxCol = board.getMaxCol()
        row = self.getRow()
        col = self.getCol()
        temp = []
        smaller = min(row, col)
        for i in range(1, smaller + 1):
            if (row - i, col - i) in blocked:
                break
            elif (row - i, col - i) not in threats:
                threats.append((row - i, col - i))
            temp.append((row - i, col - i))
        smaller = min(row, maxCol - col - 1)
        for i in range(1, smaller + 1):
            if (row - i, col + i) in blocked:
                break
            elif (row - i, col + i) not in threats:
                threats.append((row - i, col + i))
            temp.append((row - i, col + i))
        smaller = min(maxRow - row - 1, col)
        for i in range(1, smaller + 1):
            if (row + i, col - i) in blocked:
                break
            elif (row + i, col - i) not in threats:
                threats.append((row + i, col - i))
            temp.append((row + i, col - i))    
        smaller = min(maxRow - row - 1, maxCol - col - 1)
        for i in range(1, smaller + 1):
            if (row + i, col + i) in blocked:
                break
            elif (row + i, col + i) not in threats:
                threats.append((row + i, col + i))
            temp.append((row + i, col + i)) 
        # if (row, col) not in blocked:
        #     blocked.append((row, col))
        #temp.remove((row, col))
        temp = list(filter((row, col).__ne__, temp))
        assignedThreats[(row, col)] = temp
        enemies[(row, col)] = 'Bishop'

class Rook(Piece):
    def __init__(self, row, column):
        super().__init__('Rook', row, column, None)
    
    #blocks out positions where the enemy can threaten my piece and also block out the piece that it is currently on
    def putThreats(self, board):
        threats = board.getThreats()
        blocked = board.getBlocked()
        assignedThreats = board.getAssignedThreats()
        enemies = board.getEnemy()
        maxRow = board.getMaxRow()
        maxCol = board.getMaxCol()
        row = self.getRow()
        col = self.getCol()
        temp = []
        for i in range(row - 1, -1, -1):
            if (i, col) in blocked:
                break
            elif (i, col) not in threats:
                threats.append((i, col))
            temp.append((i, col))
        for i in range(row + 1, maxRow):
            if(i, col) in blocked:
                break
            elif (i, col) not in threats:
                threats.append((i, col)) 
            temp.append((i, col))
        for i in range(col + 1, maxCol):
            if (row, i) in blocked:
                break
            elif (row, i) not in threats:
                threats.append((row, i))
            temp.append((row, i))
        for i in range(col - 1, -1, -1):
            if (row, i) in blocked:
                break
            elif (row, i) not in threats:
                threats.append((row, i))
            temp.append((row, i))
        
        # if (row, col) not in blocked:
        #     blocked.append((row, col))
        #temp.remove((row, col))
        temp = list(filter((row, col).__ne__, temp))
        assignedThreats[(row, col)] = temp
        enemies[(row, col)] = 'Rook'
        
class Queen(Piece):
    def __init__(self, row, column):
        super().__init__('Queen', row, column, None)  

    #blocks out positions where the enemy can threaten my piece and also block out the piece that it is currently on
    def putThreats(self, board):
        threats = board.getThreats()
        blocked = board.getBlocked()
        assignedThreats = board.getAssignedThreats()
        enemies = board.getEnemy()
        maxRow = board.getMaxRow()
        maxCol = board.getMaxCol()
        row = self.getRow()
        col = self.getCol()
        temp = []
        for i in range(maxRow - 1, -1, -1):
            if (i, col) in blocked:
                break
            elif (i, col) not in threats:
                threats.append((i, col))
            temp.append((i, col))
        for i in range(row + 1, maxRow):
            if(i, col) in blocked:
                break
            elif (i, col) not in threats:
                threats.append((i, col))
            temp.append((i, col)) 
        for i in range(col + 1, maxCol):
            if (row, i) in blocked:
                break
            elif (row, i) not in threats:
                threats.append((row, i))
            temp.append((row, i))
        for i in range(maxCol - 1, -1, -1):
            if (row, i) in blocked:
                break
            elif (row, i) not in threats:
                threats.append((row, i))
            temp.append((row, i))
        smaller = min(row, col)
        for i in range(1, smaller + 1):
            if (row - i, col - i) in blocked:
                break
            elif (row - i, col - i) not in threats:
                threats.append((row - i, col - i))
            temp.append((row - i, col - i))
        smaller = min(row, maxCol - col - 1)
        for i in range(1, smaller + 1):
            if (row - i, col + i) in blocked:
                break
            elif (row - i, col + i) not in threats:
                threats.append((row - i, col + i))
            temp.append((row - i, col + i))
        smaller = min(maxRow - row - 1, col)
        for i in range(1, smaller + 1):
            if (row + i, col - i) in blocked:
                break
            elif (row + i, col - i) not in threats:
                threats.append((row + i, col - i))
            temp.append((row + i, col - i))    
        smaller = min(maxRow - row - 1, maxCol - col - 1)
        for i in range(1, smaller + 1):
            if (row + i, col + i) in blocked:
                break
            elif (row + i, col + i) not in threats:
                threats.append((row + i, col + i))
            temp.append((row + i, col + i)) 
        # if (row, col) not in blocked:
        #     blocked.append((row, col))
        #temp.remove((row, col))
        temp = list(filter((row, col).__ne__, temp))
        assignedThreats[(row, col)] = temp
        enemies[(row, col)] = 'Queen'



class Board:
    #populate the board with Empty space
    def __init__(self, row, col): 
        self.row = row
        self.col = col
        self.blocked = [] # all blocked which includes obstacles
        self.threats = [] # all positions that threatens
        self.board = {}
        for i in range(row):
            for j in range(col):
                self.board[(i, j)] = (1, None) # adding the normal cost of 1 and the previous piece that was traversed before this
        self.goals = [] # add goal state if there is
        self.assignedthreats = {} # assigns the row, col of an enemies to all the threats it gives
        self.enemies = {}

    def getThreats(self):
        return self.threats
    
    def getBlocked(self):
        return self.blocked

    def getMaxRow(self):
        return self.row

    def getMaxCol(self):
        return self.col

    def getAssignedThreats(self):
        return self.assignedthreats
    
    def reassignThreats(self): # readjust all the threats after removing one enemy piece
        newThreats = []
        newEnemies = {}
        for k, v in self.assignedthreats.items():
            for i in v:
                newThreats.append(i)
        for k, v in self.enemies.items():
            newEnemies[k] = v
        self.threats = newThreats
        self.enemies = newEnemies

    def addEnemy(self, index, listofenemies, enemyname):
        threat = listofenemies[index]
        name = enemyname[index]
        self.assignedthreats[index] = threat
        self.enemies[index] = name

    def getSelfThreats(self):
        counter = 0
        keys = self.assignedthreats.keys() # get all the places where there is an enemy
        temp = self.assignedthreats
        #print(temp)
        for k, v in temp.items(): # check all enemies(keys)
            #print(k, v)
            for key in keys:
                if key in v:
                    counter += 1
        return counter

    def removeEnemy(self, key):
        del self.assignedthreats[key]
        del self.enemies[key]

    def getEnemy(self):
        return self.enemies

    def __repr__(self):
        matrix = []
        for _ in range(self.row):
            r = []
            for _ in range(self.col):
                r.append(" ")
            matrix.append(r)
        for blockedPos in self.blocked:
            rw = blockedPos[0]
            cl = blockedPos[1]
            matrix[rw][cl] = 'B'
        for enemyPos in self.assignedthreats:
            rw = enemyPos[0]
            cl = enemyPos[1]
            pieceName = self.enemies[(rw, cl)]
            if (pieceName == 'King'):
               matrix[rw][cl] = "K"
            elif (pieceName == 'Queen'):
               matrix[rw][cl] = "Q"
            elif (pieceName == 'Rook'):
               matrix[rw][cl] = "R"
            elif (pieceName == 'Bishop'):
               matrix[rw][cl] = "Bi"
            elif (pieceName == 'Knight'):
               matrix[rw][cl] = "Kn"
        result = ""
        for row in matrix:
            result += str(row) + '\n'
        return result


def search(chessboard, k):
    enemies = chessboard.getAssignedThreats()
    enemylocation = list(enemies.keys())
    nameEnemies = chessboard.getEnemy()
    numEnemies = len(chessboard.getAssignedThreats())
    numRemoves = numEnemies - k
    numOfChessboards = 1
    flag = True
    counterA = 0
    lowesth = chessboard.getSelfThreats()
    while flag:
        chessboards = []
        # creation of random chessboards
        counterA = 0
        while counterA < numOfChessboards:
            samples = random.sample(range(0, numEnemies - 1), numRemoves)
            newchessboard = copy.deepcopy(chessboard)
            j = 0
            for key in enemylocation:
                if j in samples:
                    newchessboard.removeEnemy(key)
                j +=1
            newchessboard.reassignThreats()
            newh = newchessboard.getSelfThreats()
            # if newh <= lowesth:
            #     print('push new chessboard')
            chessboards.append((newh, newchessboard))
            counterA += 1
            # lowesth = newh
        flag1 = True
        pq = []
        while flag1:
            pq.clear()
            idx = 0
            # push all neightbours of each created chessboards to the pq 
            for node in chessboards:
                currh = node[0]
                chessboard1 = node[1]
                for key1 in chessboard1.getAssignedThreats().keys():
                    idx += 1
                    newchessboard1 = copy.deepcopy(chessboard1)
                    newchessboard1.removeEnemy(key1)
                    pirate = True
                    while pirate:
                        p = random.randint(1, numEnemies - 1)
                        newEnemy = enemylocation[p]
                        if newEnemy not in newchessboard1.getAssignedThreats().keys():
                            newchessboard1.addEnemy(newEnemy, enemies, nameEnemies)
                            pirate = False
                            break
                    newchessboard1.reassignThreats()
                    h = newchessboard1.getSelfThreats()
                    if h <= currh:# only if better then current state then we push
                        print('push into pq')
                        numOfPieces = len(newchessboard1.getAssignedThreats().keys())
                        heapq.heappush(pq, (h, idx, numOfPieces, newchessboard1))
            top = []
            z = 0
            # now take the best neighbouring states
            while pq:
                #print('len of pq is :', len(pq))
                goodstate = heapq.heappop(pq)
                if goodstate[0] == 0: # check if goal is reached
                    newdict = dict()
                    goalChessboard = goodstate[3]
                    #print(goalChessboard)
                    for k1, v1 in goalChessboard.getEnemy().items():
                        col = numToAlpha(k1[1])
                        row = k1[0]
                        newdict[(col, row)] = v1
                    return newdict
                else: # add to the list of top 10 states
                    top.append((goodstate[0], goodstate[3]))  
                    print('best new state added into chessboards')
                    z += 1
                    if z == 1: # break when it hits 10 states
                        print('break pq')
                        break 
            newchessboards = []
            if top:
                for newstate in top:
                    print(newstate)
                    newchessboards.append(newstate)
                chessboards = newchessboards
                print('reassigned new chessboard')
            else:
                flag1 = False
                #print('nothing new so restart the creation of chessboard')







# def search(chessboard, k):
#     enemies = chessboard.getAssignedThreats()
#     enemylocation = list(enemies.keys())
#     nameEnemies = chessboard.getEnemy()
#     numEnemies = len(chessboard.getAssignedThreats())
#     numRemoves = numEnemies - k
#     numOfChessboards = 10
#     flag = True
#     while flag:
#         chessboards = []
#         # creation of random chessboards
#         for i in range(numOfChessboards):
#             samples = random.sample(range(0, numEnemies - 1), numRemoves)
#             newchessboard = copy.deepcopy(chessboard)
#             #newthreats = (newchessboard.getAssignedThreats())
#             #toBeRemoved = []
#             j = 0
#             for key in enemylocation:#newthreats.keys():
#                 if j in samples:
#                     #toBeRemoved.append(key)
#                     newchessboard.removeEnemy(key)
#                 j +=1
#             # for m in toBeRemoved:
#             #     newchessboard.removeEnemy(m)
#             #     newchessboard.reassignThreats()
#             newchessboard.reassignThreats()
#             newh = newchessboard.getSelfThreats()
#             chessboards.append((newh, newchessboard))
#         flag1 = True
#         pq = []
#         while flag1:
#             pq.clear()
#             idx = 0
#             # push all neightbours of each created chessboards to the pq 
#             for node in chessboards:
#                 currh = node[0]
#                 chessboard1 = node[1]
#                 # boardthreats = chessboard1.getAssignedThreats()
#                 # boardthreatskeys = list(boardthreats.keys())
#                 # num = len(boardthreats.keys())
#                 # u = random.randint(0 , num - 1)
#                 # key1 = boardthreatskeys[u]
#                 #print('checking chessboard')
#                 for key1 in chessboard1.getAssignedThreats().keys():
#                     idx += 1
#                     newchessboard1 = copy.deepcopy(chessboard1)
#                     newchessboard1.removeEnemy(key1)
#                     pirate = True
#                     while pirate:
#                         p = random.randint(1, numEnemies - 1)
#                         newEnemy = enemylocation[p]
#                         if newEnemy not in newchessboard1.getAssignedThreats().keys():
#                             newchessboard1.addEnemy(newEnemy, enemies, nameEnemies)
#                             pirate = False
#                             break
#                     newchessboard1.reassignThreats()
#                     h = newchessboard1.getSelfThreats()
#                     if h <= currh:
#                         numOfPieces = len(newchessboard1.getAssignedThreats().keys())
#                         heapq.heappush(pq, (h, idx, numOfPieces, newchessboard1))
#             top10 = []
#             z = 0
#             # now take the best 10 or less neighbouring states
#             flag2 = True
#             while pq:
#                 #print('len of pq is :', len(pq))
#                 goodstate = heapq.heappop(pq)
#                 if goodstate[0] == 0: # check if goal is reached
#                     newdict = dict()
#                     goalChessboard = goodstate[3]
#                     #print(goalChessboard)
#                     for k1, v1 in goalChessboard.getEnemy().items():
#                         col = numToAlpha(k1[1])
#                         row = k1[0]
#                         newdict[(col, row)] = v1
#                     return newdict
#                 else: # add to the list of top 10 states
#                     top10.append((goodstate[0], goodstate[3]))  
#                     z += 1
#                     if z == 9: # break when it hits 10 states
#                         break 
#             samples2 = random.sample(range(0, numEnemies - 1), numRemoves)
#             newchessboard2 = copy.deepcopy(chessboard)
#             newthreats2 = (newchessboard.getAssignedThreats())
#             toBeRemoved2 = []
#             j = 0
#             for key2 in newthreats2.keys():
#                 if j in samples2:
#                     toBeRemoved2.append(key2)
#                 j +=1
#             for mp in toBeRemoved2:
#                 newchessboard2.removeEnemy(mp)
#                 newchessboard2.reassignThreats()
#             theh = newchessboard2.getSelfThreats()
#             newchessboards = []
#             newchessboards.append((theh, newchessboard2))
#             if top10:
#                 for newstate in top10:
#                     newchessboards.append(newstate)
#                 chessboards = newchessboards
#             else:
#                 flag1 = False



# def search(chessboard, k):
#     numEnemies = len(chessboard.getAssignedThreats())
#     numRemoves = numEnemies - k
#     numOfChessboards = 10
#     flag = True
#     while flag:
#         chessboards = []
#         # creation of random chessboards
#         for i in range(numOfChessboards):
#             y = random.randint(1, numRemoves)
#             samples = random.sample(range(0, numEnemies - 1), y)
#             newchessboard = copy.deepcopy(chessboard)
#             newthreats = (newchessboard.getAssignedThreats())
#             toBeRemoved = []
#             j = 0
#             for key in newthreats.keys():
#                 if j in samples:
#                     toBeRemoved.append(key)
#                 j+=1
#             for m in toBeRemoved:
#                 newchessboard.removeEnemy(m)
#                 newchessboard.reassignThreats()
#             chessboards.append(newchessboard)
#         flag1 = True
#         pq = []
#         while flag1:
#             pq.clear()
#             idx = 0
#             # push all neightbours of each created chessboards to the pq 
#             for chessboard1 in chessboards:
#                 #print('checking chessboard')
#                 for key1 in chessboard1.getAssignedThreats().keys():
#                     idx += 1
#                     newchessboard1 = copy.deepcopy(chessboard1)
#                     newchessboard1.removeEnemy(key1)
#                     newchessboard1.reassignThreats()
#                     h = newchessboard1.getSelfThreats()
#                     numOfPieces = len(newchessboard1.getAssignedThreats().keys())
#                     if numOfPieces < k:
#                         continue
#                     #print('numofpieces :', numOfPieces)
#                     heapq.heappush(pq, (h, idx, numOfPieces, newchessboard1))
#             top10 = []
#             z = 0
#             # now take the best 10 or less neighbouring states
#             flag2 = True
#             while pq:
#                 #print('len of pq is :', len(pq))
#                 goodstate = heapq.heappop(pq)
#                 # if goodstate[2] < k: # skips states where there are less than k pieces
#                 #     print('here')
#                 #     continue
#                 if goodstate[0] == 0: # check if goal is reached
#                     # flag1 = False
#                     # flag = False
#                     newdict = dict()
#                     goalChessboard = goodstate[3]
#                     #print(goalChessboard)
#                     for k1, v1 in goalChessboard.getEnemy().items():
#                         col = numToAlpha(k1[1])
#                         row = k1[0]
#                         newdict[(col, row)] = v1
#                     return newdict
#                 else: # add to the list of top 10 states
#                     top10.append(goodstate[3])
#                     z += 1
#                     if z == 10: # break when it hits 10 states
#                         break 
#             newchessboards = []
#             if top10:
#                 for newstate in top10:
#                     newchessboards.append(newstate)
#                 chessboards = newchessboardsya 
#             else:
#                 flag1 = False
            



            
                    


# def search(chessboard, k):
#     numEnemies = len(chessboard.getAssignedThreats())
#     print(numEnemies)
#     numRemoves = numEnemies - k 
#     print(numRemoves)
#     numOfChessboards = 20
#     finalEnemy = dict()
#     flag = True
#     while flag:
#         #creating 10 random chessboards
#         chessboards = []
#         for i in range(numOfChessboards):
#             print(i)
#             y = random.randint(1, numRemoves)
#             print("number of removal: ",k)
#             print("number of enemies :", numEnemies - 1)
#             samples = random.sample(range(0, numEnemies - 1), y)
#             print(samples)
#             newchessboard = copy.deepcopy(chessboard)
#             newthreats = (newchessboard.getAssignedThreats())
#             toBeRemoved = []
#             j = 0
#             for key in newthreats.keys():
#                 if j in samples:
#                     toBeRemoved.append(key)
#                 j+=1
#             for m in toBeRemoved:
#                 newchessboard.removeEnemy(m)
#                 newchessboard.reassignThreats()
#             chessboards.append(newchessboard)
            
#         for chessboard1 in chessboards:
#             print('im here')
#             enemies = dict()
#             state = []
#             state.append(chessboard1)
#             numEnemies1 = len(chessboard1.getAssignedThreats())
#             print(numEnemies1)
#             pq = []
#             temp = []
#             idx = 0
#             flag1 = True
#             n = k
#             while numEnemies1 > n:
#                 pq.clear()
#                 temp.clear()
#                 for j in state:
#                     for i in j.getAssignedThreats().keys():
#                         idx += 1
#                         newchessboard1 = copy.deepcopy(j)
#                         newchessboard1.removeEnemy(i)
#                         newchessboard1.reassignThreats()
#                         h = newchessboard1.getSelfThreats()
#                         heapq.heappush(pq, (h, idx, newchessboard1))
#                 numEnemies1 -= 1
#                 bestState = heapq.heappop(pq)
#                 if bestState[0] == 0:
#                     print('goal reached')
#                     enemies = bestState[2].getEnemy()
#                     flag1 = False #Goal State
#                     break
#                 else:
#                     temp.append(bestState[2])
#                 if n == numEnemies1:
#                     enemies = bestState[2].getEnemy()
#                     break
#                 state.clear()
#                 state = copy.deepcopy(temp)
#             if flag1 == False:
#                 finalEnemy = enemies
#                 flag = False
#                 break
        
#     newdict = dict()
#     for k, v in finalEnemy.items():
#         print(k)
#         col = numToAlpha(k[1])
#         row = k[0]
#         newdict[(col, row)] = v
#     return newdict




### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    # testfile = sys.argv[1] #Do not remove. This is your input testfile.
    testfile = "allHorse.txt"
    f = open(testfile, "r")
    txt_file = f.read().split("\n")
    noOfRows = int(txt_file[0].split(":")[1])
    noOfCols = int(txt_file[1].split(":")[1])
    noOfObstacles = int(txt_file[2].split(":")[1])
    chessboard = Board(noOfRows, noOfCols)
    if noOfObstacles != 0:
        obstacles = str(txt_file[3][38:]).split(' ')
        for obstacle in obstacles:
            row = int(obstacle[1:])
            col = alphaToNum(obstacle[0])
            chessboard.blocked.append((row, col))

    k = int(txt_file[4].split(":")[1])
    temp = []
    #print(len(txt_file))
    for i in range(7, len(txt_file) - 1):
        # if txt_file[i][0] == "[":
        #print('enemy added')
        opponent_type = txt_file[i].split(',')[0][1:]
        col = alphaToNum(txt_file[i].split(',')[1][0])
        row = int(txt_file[i].split(",")[1][1:-1])
        temp.append([row, col, opponent_type])
        #print([row, col, opponent_type])
        # else:
        #     break
    # for i in range(len(temp)):
    #     blocked = chessboard.getBlocked()
    #     blocked.append((temp[i][0], temp[i][1]))
    for i in range(len(temp)):
        opponent_type = temp[i][2]
        row = temp[i][0]
        col = temp[i][1]
        if opponent_type == 'Queen':
            #print('queen added')
            enemy = Queen(row, col)
        elif opponent_type == 'King':
            #print('king added')
            enemy = King(row, col)
        elif opponent_type == 'Rook':
            enemy = Rook(row, col)
        elif opponent_type == 'Bishop':
            enemy = Bishop(row, col)
        elif opponent_type == 'Knight':
            #print('knight added')
            enemy = Knight(row, col)
        enemy.putThreats(chessboard)
        #print(chessboard.assignedthreats)
    #print(chessboard.getAssignedThreats())
    goalState = search(chessboard, k)
    print(goalState)
    return goalState #Format to be returned
t0 = time()
print(run_local())
print(time() - t0)