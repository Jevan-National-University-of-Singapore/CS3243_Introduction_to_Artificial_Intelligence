import sys
import random
import copy
import heapq
# from time import time
def splitt(word):
    head = word.rstrip('0123456789')
    tail = word[len(head):]
    lst = [head,tail]
    return(lst)
def my_func(path): #change to remove the priority first
    my_ans = []
    for i in range(1,len(path)):
        if i != len(path) - 1:
            my_ans.append([path[i],path[i+1]])
    return(my_ans)
def my_funcc(lst_of_lst):
    my_ans = {}
    for y, x in lst_of_lst:
        my_ans[(chr(x+97),y)] = lst_of_lst[(y, x)]                    
    return my_ans

def withinBoard(max_row, max_column, x, y):
    return 0<=x<max_row and 0<=y<max_column
# my_lst[piece], piece, blok, my_lst, row, col
def threateningThreat(piece_type, piece_position, blocked, max_row, max_column):
    # print(my_ll)       #row by col is key, value is piecetype
    threatened = set()
    piece_x, piece_y = piece_position
    if piece_type == "King":
        legal_x = [-1,    0,   1,   -1,    1,   -1,     0,      1]
        legal_y = [-1,    -1,  -1,   0,     0,  1,      1,      1,]
        index = 0
        for x in legal_x:
            y = legal_y[index]
            if withinBoard(max_row, max_column, piece_x + x, piece_y + y):
                threatened.add((piece_x+x, piece_y+y))
            index += 1
                        
                        
    elif piece_type == "Knight":
        legal_x = [-2, -1, -2, -1, 2, 1, 2, 1]
        legal_y = [-1, -2, 1, 2, -1, -2, 1, 2]
        index = 0
        for x in legal_x:
            y = legal_y[index]
            if withinBoard(max_row, max_column, piece_x + x, piece_y + y):
                threatened.add((piece_x+x, piece_y+y))
            index += 1
                        
    elif piece_type == "Rook":
        for i in range(piece_x+1, max_row):
            threatened.add((i,piece_y))
            if (i, piece_y) in blocked:
                break
            

        for i in range(piece_y+1, max_column):
            threatened.add((piece_x,i))
            if (piece_x, i) in blocked:
                break
           
                
        for i in range(1, piece_x+1):
            threatened.add((piece_x-i,piece_y))
            if (piece_x-i, piece_y) in blocked:
                break
           

        for i in range(1, piece_y+1):
            threatened.add((piece_x,piece_y-i))
            if (piece_x, piece_y-i) in blocked:
                break

    elif piece_type == "Bishop":
        my_x = piece_x - 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x -= 1
            my_y -= 1
        
        my_x = piece_x + 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x += 1
            my_y -= 1

        my_x = piece_x - 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x -= 1
            my_y += 1

        my_x = piece_x + 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x += 1
            my_y += 1
    elif piece_type == 'Queen':
        my_x = piece_x - 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x -= 1
            my_y -= 1
        
        my_x = piece_x + 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x += 1
            my_y -= 1

        my_x = piece_x - 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x -= 1
            my_y += 1

        my_x = piece_x + 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            threatened.add((my_x,my_y))
            if (my_x,my_y) in blocked:
                break
            my_x += 1
            my_y += 1

        for i in range(piece_x+1, max_row):
            threatened.add((i,piece_y))
            if (i, piece_y) in blocked:
                break
            

        for i in range(piece_y+1, max_column):
            threatened.add((piece_x,i))
            if (piece_x, i) in blocked:
                break
           
                
        for i in range(1, piece_x+1):
            threatened.add((piece_x-i,piece_y))
            if (piece_x-i, piece_y) in blocked:
                break
           

        for i in range(1, piece_y+1):
            threatened.add((piece_x,piece_y-i))
            if (piece_x, piece_y-i) in blocked:
                break
        
        
                
    return threatened
        
        
        
            
            
        
def heuristic_value(row,col,my_lst,my_obs):
    # Calculates the heuristic value h of the current state of board
    # Number of pairs of queens attacking each other directly or indirectly
    h = 0
    blok = my_obs.copy()
    for piece in my_lst:
        blok.add(piece)
    
    for piece in my_lst:
        threatening_threat = threateningThreat(my_lst[piece], piece, blok, row, col)
        for piece in my_lst:
            if piece in threatening_threat:
                
                h+=1
            
    return h
        

def neighbour(row,col,my_ll,my_h,D,E, obstacles): #return the gameboard with 1 less piece and least h
    lower_list = []
    equal_list = []
    higher_list = []
    counter = 0
    for piece in my_ll:
        randomness = random.random()
        if randomness < D/E:#0.9:
            ll = copy.deepcopy(my_ll)
            ll.pop(piece)
            cost = heuristic_value(row,col,ll, obstacles)
            if cost == 0:
                return "found",counter, ll
            if cost < my_h:
                lower_list.append((cost, counter, ll))
            elif cost == my_h:
                equal_list.append((cost, counter, ll))
            else:
                higher_list.append((cost, counter, ll))
        counter += 1

            
    successor = None

    if lower_list:
        heapq.heapify(lower_list)
        successor = heapq.heappop(lower_list)
    elif equal_list:
        successor = equal_list[0]
    elif higher_list:
        randomness = random.random()
        if randomness < D/E:
            successor = random.choice(higher_list)
    
    
    return successor
      
                
def parsePieceLine(line, coor): 
    piece, pos = line[1:-2].split(",")
    x = ord(pos[0])-97
    y = int(pos[1:])
    coor[(y, x)] = piece

def parseObjectLine(line, obstacles):
    line.strip("\n")
    for pos in line.split():
        x = ord(pos[0])-97
        y = int(pos[1:])
        obstacles.add((y, x))
                
                
                       
    
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)
 
# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    file = sys.argv[1] #Do not remove. This is your input testfile.
    # file = "Local2.txt"
    rows = 0
    cols = 0
    list_of_enemies = 0
    K_value = 0
    num_of_enemy = 0
    coor_global = {}
    obs_set = set()
    with open(file,'r') as data_file:
        
        for line in data_file:
            
            data = line.split(':')
            
            if data[0] == "Rows":
                rows = int(data[1])
                
            elif data[0] == "Cols":
                cols = int(data[1])
                
            elif data[0] == "Number of Obstacles":
                obs = data[1]
                
            elif data[0] == "Position of Obstacles (space between)":
                if data[1] != '-\n':
                    for a in data[1].strip().split(' '):
                        parseObjectLine(data[1], obs_set)
                    
            elif data[0] == "Number of King, Queen, Bishop, Rook, Knight (space between)":
                list_of_enemies = data[1].strip().split(' ')
                num_of_enemy = int(list_of_enemies[0]) + int(list_of_enemies[1]) + int(list_of_enemies[2]) + int(list_of_enemies[3]) + int(list_of_enemies[4])
                
            elif data[0] == "K (Minimum number of pieces left in goal)":
                K_value = int(data[1])
            elif data[0].find('King') == True :
                parsePieceLine(data[0], coor_global)
                
            elif data[0].find('Queen') == True :
                parsePieceLine(data[0], coor_global)
                
            elif data[0].find('Knight') == True :
                parsePieceLine(data[0], coor_global)
             
            elif data[0].find('Bishop') == True :
                parsePieceLine(data[0], coor_global)
                
            elif data[0].find('Rook') == True :
                parsePieceLine(data[0], coor_global)
            elif data[0] == "Step cost to move to selected grids (Default cost is 1) [Pos, Cost]":
                continue
            elif data[0] == "Starting Position of Pieces [Piece, Pos]":
                continue
            elif data[0] == "Position of Enemy Pieces":
                continue
 
    data_file.close()
    
    
      
    ##obs_set now has piece position and obstacle position of the initial board
 #row by col y by x
    #hill climb
    # while True:
    for z in range(60):
        randomm = random.choice(range(K_value,num_of_enemy))
        cor = {}
        enemies_pos_random = random.sample(list(coor_global),randomm)
        for random_enemy in enemies_pos_random:
            cor[random_enemy] = coor_global[random_enemy]

        current_K = len(cor)
        
    
        while current_K > K_value:
        
            value_now = heuristic_value(rows,cols,cor,obs_set)
    
            a = copy.deepcopy(cor)
            succ = neighbour(rows,cols,a,value_now,K_value,current_K,obs_set)
            if succ:
                if succ[0] == "found":
                    return my_funcc(succ[2])
                else:        
                    cor = succ[2]
                    current_K -= 1
               
                    
                    
       
    
# t0 = time() 
# print(run_local())
# print(time() - t0)
'''
python /Users/lockmeilin/Downloads/CS3/Project\ 2/Local.py /Users/lockmeilin/Downloads/CS3/Project\ 2/Public\ Testcases/Local1.txt 

'''
