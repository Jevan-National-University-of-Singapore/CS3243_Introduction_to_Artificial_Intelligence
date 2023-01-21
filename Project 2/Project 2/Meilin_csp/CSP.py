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
def my_funcc(dictt):
    my_ans = {}
    
    for i in dictt:#i
        #my_ans[(chr(x+97),y)] = 
        my_ans[(chr(i[1]+97),i[0])] = dictt[(i[0], i[1])]                    
    return my_ans
 
def withinBoard(max_row, max_column, x, y):
    return 0<=x<max_row and 0<=y<max_column
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
# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    # file = sys.argv[1] #Do not remove. This is your input testfile.
    file = "CSP10.txt"
    ###csp
    rows = 0
    cols = 0
    obs = 0
    pos_obs = []
    step_costs = []
    list_of_enemies = 0
    enemies_pos = []
    num_own = 0
    my_pos = []
    num_of_enemy = 0
    obs_set = set()
    # coor = {"King": set(), "Queen": set(), "Bishop": set(), "Rook": set(), "Knight": set()}
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
                        parseObjectLine(data[1],obs_set)
                    
            elif data[0] == "Number of King, Queen, Bishop, Rook, Knight (space between)":
                list_of_enemies = data[1].strip().split(' ')
                num_of_enemy = int(list_of_enemies[0]) + int(list_of_enemies[1]) + int(list_of_enemies[2]) + int(list_of_enemies[3]) + int(list_of_enemies[4])
            
 
    data_file.close()
    
    coor = {'total':num_of_enemy,'King':int(list_of_enemies[0]),'Queen':int(list_of_enemies[1]),'Rook':int(list_of_enemies[3]),'Bishop':int(list_of_enemies[2]),'Knight':int(list_of_enemies[4])}
                    
    for obstacle in pos_obs:
 
        handle = obstacle #i0
 
        x = splitt(handle)[0]#i
        
        if len(x) > 0:
 
            x = ord(x) - 97 #i = 8
 
            y = splitt(handle)[1]
 
            if len(y) > 0:
                

                obs_set.add((int(y),int(x)))
  
    #coor is initally a dict of all the pieces position {'total': 16...}
    #num_of_enemy is if 16 0 4 0 3, 23
    #obs_set is a set of tuple board position without obstacles(but not without pieces?)
    #added_pos is a dict of key positions value piece type,initially empty
    valid_positions = set()#a set of pos without obs
    added_pos = {} 
    hash_value = frozenset()
    for i in range(cols):
        for j in range(rows):
            if (j,i) not in obs_set:
                valid_positions.add((j,i))
    my_stack = [(added_pos,valid_positions,coor, hash_value)]
    visited = {hash_value}
    explored_pieces = {}
    while my_stack:
        hand = my_stack.pop()
        added = hand[0]
        valid = hand[1]
        remaining = hand[2]
        hash_value = hand[3]
           
        add_piece_type = "omae wa piece type ga..."
    
        if remaining['total'] == 0 :
            return my_funcc(added)
        if remaining["Queen"] > 0:
            add_piece_type = "Queen"
        elif remaining["Rook"] > 0:
            add_piece_type = "Rook"
        elif remaining["Bishop"] > 0:
            add_piece_type = "Bishop"
        elif remaining["Knight"] > 0:
            add_piece_type = "Knight"
        else:
            add_piece_type = "King"
    
        for position in valid:
            new_hash_value = frozenset.union(hash_value, {(position, add_piece_type)})
            if new_hash_value not in visited:
                visited.add(new_hash_value)        
                if (position, add_piece_type) not in explored_pieces:
                    explored_pieces[(position, add_piece_type)] = threateningThreat(add_piece_type,position,obs_set,rows,cols)

                threat_positions = explored_pieces[(position, add_piece_type)]


                violates = False   
                for pieces in added:
                    if pieces in threat_positions:
                        violates = True
                        break
                if violates == False:
                    #add piece to idct of added
                    
                    added_copy = copy.copy(added)
                    valid_copy = copy.copy(valid)
                    added_copy[(position)] = add_piece_type
                    if remaining["total"] == 1:
                        return my_funcc(added_copy)
                    #remove pos and added_piece's threatening pos from the set of valid
                    valid_copy.remove((position))
                    threat_positions = threateningThreat(add_piece_type,position,obs_set,rows,cols)
                    # for i in threat_positions:
                    #     if i not in obs_set and i in valid_copy: 
                            
                    valid_copy -= threat_positions
                    #remove from remaining pieces(coor)
                    remaining_copy = copy.copy(remaining)
                    remaining_copy[add_piece_type] -= 1
                    remaining_copy['total'] -= 1
                    #push available_pos,add,remaining back to frontier
                    my_stack.append([added_copy,valid_copy,remaining_copy, new_hash_value])
                                
            
                
                    
            
        
        
    
    
print(run_CSP())

    
    
    
