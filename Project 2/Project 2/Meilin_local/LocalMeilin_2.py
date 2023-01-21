import sys
import random
import copy
import heapq
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
    for x, y in lst_of_lst:
        my_ans[(chr(x+97),y)] = lst_of_lst[(x, y)]                    
            
    return my_ans

def withinBoard(max_row, max_column, x, y):
    return 0<=x<max_row and 0<=y<max_column

def threateningThreat(piece_type, piece_position, blocked, my_ll, max_row, max_column):
    threatened = set()
    piece_x, piece_y = piece_position
    if piece_type == "King":
        legal_x = [-1,0,1,-1,1,-1,0,1]
        legal_y = [-1,0,1,-1,1,-1,0,1]
        for i in range(len(legal_x)):
            if withinBoard(max_row, max_column, piece_x + legal_x(i), piece_y + legal_y[i]):
                for types in my_ll:
                    if (piece_x, piece_y) in types:
                        threatened.add((piece_x, piece_y))
                        
                        
    elif piece_type == "Knight":
        legal_x = [-2, -1, -2, -1, 2, 1, 2, 1]
        legal_y = [-1, -2, 1, 2, -1, -2, 1, 2]
        for i in range(len(legal_x)):
            if withinBoard(max_row, max_column, piece_x + legal_x(i), piece_y + legal_y[i]):
                for types in my_ll:
                    if (piece_x, piece_y) in types:
                        threatened.add((piece_x, piece_y))
                        
    elif piece_type == "Rook":
        for i in range(piece_x+1, max_row):
            if (i, piece_y) in blocked:
                break
            else:
                threatened.add((i, piece_y))


        for i in range(piece_y+1, max_column):
            if (piece_x, i) in blocked:
                break
            else:
                threatened.add((piece_x, i))
                
        for i in range(0, piece_x):
            if (piece_x-i, piece_y) in blocked:
                break
            else:
                threatened.add((piece_x-i, piece_y))

        for i in range(0, piece_y):
            if (i, piece_y-i) in blocked:
                break
            else:
                threatened.add((i, piece_y-i))

    elif piece_type == "Bishop":
        my_x = piece_x - 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x -= 1
                my_y -= 1
                
        my_x = piece_x + 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x += 1
                my_y -= 1

        my_x = piece_x - 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x -= 1
                my_y += 1

        my_x = piece_x + 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x += 1
                my_y += 1
    elif piece_type == 'Queen':
        for i in range(piece_x+1, max_row):
            if (i, piece_y) in blocked:
                break
            else:
                threatened.add((i, piece_y))


        for i in range(piece_y+1, max_column):
            if (piece_x, i) in blocked:
                break
            else:
                threatened.add((piece_x, i))
                
        for i in range(0, piece_x):
            if (piece_x-i, piece_y) in blocked:
                break
            else:
                threatened.add((piece_x-i, piece_y))

        for i in range(0, piece_y):
            if (i, piece_y-i) in blocked:
                break
            else:
                threatened.add((i, piece_y-i))
        my_x = piece_x - 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x -= 1
                my_y -= 1
                
        my_x = piece_x + 1
        my_y = piece_y - 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x += 1
                my_y -= 1

        my_x = piece_x - 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x -= 1
                my_y += 1

        my_x = piece_x + 1
        my_y = piece_y + 1
        
        while withinBoard(max_row,max_column,my_x,my_y):
            if (my_x,my_y) in blocked:
                break
            else:
                threatened.add((my_x,my_y))
                my_x += 1
                my_y += 1
                
    return threatened
        
        
        
            
            
        
def heuristic_value(board,row,col,my_lst,my_obs):
    # Calculates the heuristic value h of the current state of board
    # Number of pairs of queens attacking each other directly or indirectly
    h = 0
    blok = my_obs.copy()
    for piece in my_lst:
        blok.add(piece)
    
    for piece in my_lst:
        threateningthreat = threateningThreat(my_lst[piece], piece, blok, my_lst, row, col)
        for threat in my_lst:
            if threat in threateningthreat:
                h+=1
    return h
        

def min_neighbour(board,row,col,my_ll,my_h,D,E, obstacles): #return the gameboard with 1 less piece and least h
    lower_list = []
    equal_list = []
    higher_list = []
    for piece in my_ll:
        randomness = random.random()
        if randomness < D/E:#0.9:
            piece_row = piece[0]
            piece_col = piece[1]
            bod = copy.deepcopy(board)
            bod[piece_row][piece_col] = '1'
            ll = copy.deepcopy(my_ll)
            ll.remove(piece)
            cost = heuristic_value(bod,row,col,ll, obstacles)
            if cost == 0:
                return "found"
            if cost < my_h:
                lower_list.append((cost,bod, ll))
            elif cost == my_h:
                equal_list.append((cost, bod, ll))
            else:
                higher_list.append((cost, bod, ll))

            
    successor = None

    if lower_list:
        heapq.heapify(lower_list)
        successor = heapq.heappop(lower_list)
    elif equal_list:
        successor = lower_list[0]
    elif higher_list:
        randomness = random.random()
        if randomness < D/E:
            successor = random.choice(higher_list)
    
    
    return successor
      
                
 
            
                
                
                       
    
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)
 
# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    # file = sys.argv[1] #Do not remove. This is your input testfile.
    file = "Local1.txt"
    rows = 0
    cols = 0
    obs = 0
    pos_obs = []
    step_costs = []
    list_of_enemies = 0
    enemies_pos = []
    num_own = 0
    my_pos = []
    goals = 0
    K_value = 0
    num_of_enemy = 0
    coor = {}
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
                if data[1] != '-':
                    
                    for a in data[1].strip().split(' '):
                        pos_obs.append(a)
                    
            elif data[0] == "Number of King, Queen, Bishop, Rook, Knight (space between)":
                list_of_enemies = data[1].strip().split(' ')
                num_of_enemy = int(list_of_enemies[0]) + int(list_of_enemies[1]) + int(list_of_enemies[2]) + int(list_of_enemies[3]) + int(list_of_enemies[4])
                
            elif data[0] == "K (Minimum number of pieces left in goal)":
                K_value = int(data[1])
            elif data[0].find('King') == True :
                enemies_pos.extend(data[0].split())
                
            elif data[0].find('Queen') == True :
                enemies_pos.extend(data[0].split())
                
            elif data[0].find('Knight') == True :
                enemies_pos.extend(data[0].split())
             
            elif data[0].find('Bishop') == True :
                enemies_pos.extend(data[0].split())
                
            elif data[0].find('Rook') == True :
                enemies_pos.extend(data[0].split())
            elif data[0] == "Step cost to move to selected grids (Default cost is 1) [Pos, Cost]":
                continue
            elif data[0] == "Starting Position of Pieces [Piece, Pos]":
                continue
            elif data[0] == "Position of Enemy Pieces":
                continue
 
    data_file.close()
    game_board = [['1'] * int(cols) for i in range(int(rows))]
 
    for obstacle in pos_obs:
 
        handle = obstacle #i0
 
        x = splitt(handle)[0]#i
 
        if len(x) > 0:
 
            x = ord(x) - 97 #i = 8
 
            y = splitt(handle)[1]
 
            if len(y) > 0:
 
                game_board[int(y)][int(x)] = 'x'
 
    
    for enemy in enemies_pos:
        enemy = enemy[1 : : ]
        enemy = enemy[ :-1: ]
        pos = 0
        
        if 'King' in enemy:
            temp = enemy.split(',')
            pos = temp[1]#e0
            x = splitt(pos)[0]#e
 
            if len(x) > 0:
 
                x = ord(x) - 97 #e = 4
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    coor[(y, x)] = "King"
                    game_board[y][x] = 'K'
 #row by col y by x
                   
                        
        elif "Queen" in enemy:
            temp = enemy.split(',')
            
            pos = temp[1]#c5
            x = splitt(pos)[0]#c
            
            if len(x) > 0:
 
                x = ord(x) - 97 #c = 2
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    coor[(y, x)] = "Queen"
                    game_board[y][x] = 'Q'
                    
 #row by col y by x
                    
            
            
        elif 'Rook' in enemy:
            temp = enemy.split(',')
            
            pos = temp[1]#c5
            x = splitt(pos)[0]#c
            
            if len(x) > 0:
 
                x = ord(x) - 97 #c = 2
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    coor[(y, x)] = "Rook"
                    game_board[y][x] = 'R'
                    
 #row by col y by x
                    
 
                    
 #row by col y by x
                    
 
        elif 'Bishop' in enemy:
            
            temp = enemy.split(',')
            pos = temp[1]#c5
            x = splitt(pos)[0]#c
            
            if len(x) > 0:
 
                x = ord(x) - 97 #c = 2
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    coor[(y, x)] = "Bishop"
                    game_board[y][x] = 'B'
 #row by col y by x
                    
                                        
                    
                                
        
                            
        elif 'Knight' in enemy:
            
            temp = enemy.split(',')
            pos = temp[1]#e0
            x = splitt(pos)[0]#e
 
            if len(x) > 0:
 
                x = ord(x) - 97 #e = 4
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    coor[(y, x)] = "Knight"
                    game_board[y][x] = 'N'
 #row by col y by x
    #hill climb
    KK = num_of_enemy
    current = copy.deepcopy(game_board)
    cor = coor.copy()
    
    
    timer = 0
    while KK >= K_value:
        timer += 1
        value_now = heuristic_value(current,rows,cols,cor)
        
        if value_now == 0:
            
            return my_funcc(cor)
        elif timer > 2000:
            
            return my_funcc(cor)
        elif KK == K_value:
            game_board = [['1'] * int(cols) for i in range(int(rows))]
 
            for obstacle in pos_obs:
         
                handle = obstacle #i0
         
                x = splitt(handle)[0]#i
         
                if len(x) > 0:
         
                    x = ord(x) - 97 #i = 8
         
                    y = splitt(handle)[1]
         
                    if len(y) > 0:
         
                        game_board[int(y)][int(x)] = 'x'
                        
            randomm = random.choice(range(K_value,num_of_enemy))
            coor = {}
            enemies_pos_random = random.sample(enemies_pos,randomm)
            for enemy in enemies_pos_random:
                enemy = enemy[1 : : ]
                enemy = enemy[ :-1: ]
                pos = 0
                
                if 'King' in enemy:
                    temp = enemy.split(',')
                    pos = temp[1]#e0
                    x = splitt(pos)[0]#e
         
                    if len(x) > 0:
         
                        x = ord(x) - 97 #e = 4
                        y = splitt(pos)[1]
         
                        if len(y) > 0:
         
                            y = int(y)
                            x = int(x)
                            coor[(y,x)] = "King"
                            game_board[y][x] = 'K'
         #row by col y by x
                           
                                
                elif "Queen" in enemy:
                    temp = enemy.split(',')
                    
                    pos = temp[1]#c5
                    x = splitt(pos)[0]#c
                    
                    if len(x) > 0:
         
                        x = ord(x) - 97 #c = 2
                        y = splitt(pos)[1]
         
                        if len(y) > 0:
         
                            y = int(y)
                            x = int(x)
                            coor[(y,x)] = "Queen"
                            game_board[y][x] = 'Q'
                            
         #row by col y by x
                            
                    
                    
                elif 'Rook' in enemy:
                    temp = enemy.split(',')
                    
                    pos = temp[1]#c5
                    x = splitt(pos)[0]#c
                    
                    if len(x) > 0:
         
                        x = ord(x) - 97 #c = 2
                        y = splitt(pos)[1]
         
                        if len(y) > 0:
         
                            y = int(y)
                            x = int(x)
                            coor[(y,x)] = "Rook"
                            game_board[y][x] = 'R'
                            
         #row by col y by x
                            
         
                            
         #row by col y by x
                            
         
                elif 'Bishop' in enemy:
                    
                    temp = enemy.split(',')
                    pos = temp[1]#c5
                    x = splitt(pos)[0]#c
                    
                    if len(x) > 0:
         
                        x = ord(x) - 97 #c = 2
                        y = splitt(pos)[1]
         
                        if len(y) > 0:
         
                            y = int(y)
                            x = int(x)
                            coor[(y,x)] = "Bishop"
                            game_board[y][x] = 'B'
         #row by col y by x
                            
                                                
                            
                                        
                
                                    
                elif 'Knight' in enemy:
                    
                    temp = enemy.split(',')
                    pos = temp[1]#e0
                    x = splitt(pos)[0]#e
         
                    if len(x) > 0:
         
                        x = ord(x) - 97 #e = 4
                        y = splitt(pos)[1]
         
                        if len(y) > 0:
         
                            y = int(y)
                            x = int(x)
                            coor[(y,x)] = "Knight"
                            game_board[y][x] = 'N'
                
            KK = len(coor) 
            current = game_board
            cor = coor
          
            #print("rr2")
            #print(cor)
            #print("rr2")
        else:
            a = copy.deepcopy(cor)
            succ = min_neighbour(current,rows,cols,a,value_now,K_value,KK)
            if succ == "found":
                
                return my_funcc(cor)
            elif succ:        
                current, cor = succ[1], succ[2]
                KK -= 1
            else:
                
                game_board = [['1'] * int(cols) for i in range(int(rows))]
 
                for obstacle in pos_obs:
             
                    handle = obstacle #i0
             
                    x = splitt(handle)[0]#i
             
                    if len(x) > 0:
             
                        x = ord(x) - 97 #i = 8
             
                        y = splitt(handle)[1]
             
                        if len(y) > 0:
             
                            game_board[int(y)][int(x)] = 'x'
                            
                randomm = random.choice(range(K_value,num_of_enemy))
                coor = {}
                enemies_pos_random = random.sample(enemies_pos,randomm)
                for enemy in enemies_pos_random:
                    enemy = enemy[1 : : ]
                    enemy = enemy[ :-1: ]
                    pos = 0
                    
                    if 'King' in enemy:
                        temp = enemy.split(',')
                        pos = temp[1]#e0
                        x = splitt(pos)[0]#e
             
                        if len(x) > 0:
             
                            x = ord(x) - 97 #e = 4
                            y = splitt(pos)[1]
             
                            if len(y) > 0:
             
                                y = int(y)
                                x = int(x)
                                coor[(y,x)] = "King"
                                game_board[y][x] = 'K'
             #row by col y by x
                               
                                    
                    elif "Queen" in enemy:
                        temp = enemy.split(',')
                        
                        pos = temp[1]#c5
                        x = splitt(pos)[0]#c
                        
                        if len(x) > 0:
             
                            x = ord(x) - 97 #c = 2
                            y = splitt(pos)[1]
             
                            if len(y) > 0:
             
                                y = int(y)
                                x = int(x)
                                coor[(y,x)] = "Queen"
                                game_board[y][x] = 'Q'
                                
             #row by col y by x
                                
                        
                        
                    elif 'Rook' in enemy:
                        temp = enemy.split(',')
                        
                        pos = temp[1]#c5
                        x = splitt(pos)[0]#c
                        
                        if len(x) > 0:
             
                            x = ord(x) - 97 #c = 2
                            y = splitt(pos)[1]
             
                            if len(y) > 0:
             
                                y = int(y)
                                x = int(x)
                                coor[(y,x)] = "Rook"
                                game_board[y][x] = 'R'
                                
             #row by col y by x
                                
             
                                
             #row by col y by x
                                
             
                    elif 'Bishop' in enemy:
                        
                        temp = enemy.split(',')
                        pos = temp[1]#c5
                        x = splitt(pos)[0]#c
                        
                        if len(x) > 0:
             
                            x = ord(x) - 97 #c = 2
                            y = splitt(pos)[1]
             
                            if len(y) > 0:
             
                                y = int(y)
                                x = int(x)
                                coor[(y,x)] = "Bishop"
                                game_board[y][x] = 'B'
             #row by col y by x
                                
                                                    
                                
                                            
                    
                                        
                    elif 'Knight' in enemy:
                        
                        temp = enemy.split(',')
                        pos = temp[1]#e0
                        x = splitt(pos)[0]#e
             
                        if len(x) > 0:
             
                            x = ord(x) - 97 #e = 4
                            y = splitt(pos)[1]
             
                            if len(y) > 0:
             
                                y = int(y)
                                x = int(x)
                                coor[(y,x)] = "Knight"
                                game_board[y][x] = 'N'
                    
                KK = len(KK) 
                current = game_board
                cor = coor
            # elif heuristic_value(succ,rows,cols,a) == 0:
            #     return(my_funcc(a))
               
                    
                    
       
    
 
print(run_local())
#run_local()                
'''
python /Users/lockmeilin/Downloads/CS3/Project\ 2/Local.py /Users/lockmeilin/Downloads/CS3/Project\ 2/Public\ Testcases/Local1.txt 

'''
