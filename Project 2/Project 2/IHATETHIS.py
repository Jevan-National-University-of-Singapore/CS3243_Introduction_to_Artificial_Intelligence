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
    lst_of_lst_index = 0
    for piece_type in lst_of_lst:
        for piece in piece_type:                
            y = piece[0]
            x = piece[1]
                
            if lst_of_lst_index == 0:
                my_ans[tuple((chr(x+97),y))] = 'King'
            elif lst_of_lst_index == 1:
                my_ans[tuple((chr(x+97),y))] = 'Queen'
            elif lst_of_lst_index == 2:
                my_ans[tuple((chr(x+97),y))] = 'Rook'
            elif lst_of_lst_index == 3:
                my_ans[tuple((chr(x+97),y))] = 'Bishop'
            elif lst_of_lst_index == 4:
                my_ans[tuple((chr(x+97),y))] = 'Knight'
        lst_of_lst_index += 1
                    
            
    return my_ans
            
    
 

def heuristic_value(board,row,col,my_lst):
    # Calculates the heuristic value h of the current state of board
    # Number of pairs of queens attacking each other directly or indirectly
 
    h = 0
    queen_pairs = []
    king_pairs = []
    rook_pairs = []
    bishop_pairs = []
    knight_pairs = []
    for i in range(row):
        for j in range(col):
               
            if (i,j) in my_lst[1]:
                for k in range (1,j+1):
                    if 0 <= j-k < len(board[i]) and 0 <= i < row:
                        if board[i][j-k] == 'K' or board[i][j-k] == 'Q' or board[i][j-k] == 'R' or board[i][j-k] == 'B' or board[i][j-k] == 'N':
                            queen_pairs.append((i,j,i,j-k))
                            h += 1
                            break    
                        elif board[i][j-k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                
                
                        
                for k in range (1,col-j):
                    
                    if len(board[i]) > j+k >= 0 and 0 <= i < row:
                        if board[i][j+k] == 'K' or board[i][j+k] == 'Q' or board[i][j+k] == 'R' or board[i][j+k] == 'B' or board[i][j+k] == 'N':
                            queen_pairs.append((i,j,i,j+k))
                            h += 1
                            break
                        elif board[i][j+k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                
                        
                for k in range (1,row-i):
                    if 0<= i+k < row and 0<= j < len(board[i+k]):
                        if board[i+k][j] == 'K' or board[i+k][j] == 'Q' or board[i+k][j] == 'R' or board[i+k][j] == 'B' or board[i+k][j] == 'N':
                            queen_pairs.append((i,j,i+k,j))
                            h += 1
                            break
                        elif board[i+k][j] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                
                    
                        
                for k in range (1,i+1):
                    if row > i-k >= 0 and 0<= j < len(board[i-k]):
                        if board[i-k][j] == 'K' or board[i-k][j] == 'Q' or board[i-k][j] == 'R' or board[i-k][j] == 'B' or board[i-k][j] == 'N':
                            queen_pairs.append((i,j,i-k,j))
                            h += 1
                            break
                        elif board[i-k][j] == '1':
                            continue
                            
                        else:
                            break
                    else:
                        break
                boo = True
                for k in range(row-i +1):
                    
                    if boo == True:
                        for q in range(col-j +1):
                            
                            if k == q:
                                
                                if i+k < row and j+k < col:
                                    
                                    if board[i+k][j+k] == 'K' or board[i+k][j+k] == 'Q' or board[i+k][j+k] == 'R' or board[i+k][j+k] == 'B' or board[i+k][j+k] == 'N':
                                        if k != 0:
                                        
                                            queen_pairs.append((i,j,i+k,j+k))
                                            
                                            h += 1
                                            boo = False
                                    elif board[i+k][j+k] == '1':
                                        continue
        
                                    else:
                                            
                                        boo = False
                                            
                    else:
                        break
               
                booo = True
                for k in range(i +1):
                    if booo == True:
                        for q in range(j +1):
                            if k == q:
                                if i-k >= 0 and j-k >= 0:
                                    if board[i-k][j-k] == 'K' or board[i-k][j-k] == 'Q' or board[i-k][j-k] == 'R' or board[i-k][j-k] == 'B' or board[i-k][j-k] == 'N':
                                        if k!= 0:
                                            queen_pairs.append((i,j,i-k,j-k))
                                            h += 1
                                            booo = False
                                    elif board[i-k][j-k] == '1':
                                        continue       
                                    else:
                                            
                                        booo = False
                                            
                    else:
                        break
                
                    
                boooo = True           
                for k in range(row-i +1):
                    
                    if boooo == True:
                        for q in range(j+1):
                            if k == q:
                                if i+k < row and j-k >= 0:
                                    if board[i+k][j-k] == 'K' or board[i+k][j-k] == 'Q' or board[i+k][j-k] == 'R' or board[i+k][j-k] == 'B' or board[i+k][j-k] == 'N':
                                        if k != 0:
                                            
                                            queen_pairs.append((i,j,i+k,j-k))
                                            h += 1
                                            boooo = False
                                        
                                    elif board[i+k][j-k] == '1':
                                        continue
                                    else:
                                            
                                        boooo = False
                                            
                    else:
                        break
                
                booooo = True           
                for k in range(i+1):
                        
                    if booooo == True:
                        for q in range((col-j)+1):
                            if k == q:
                                if i-k >= 0 and j+k < col:
                                    if board[i-k][j+k] == 'K' or board[i-k][j+k] == 'Q' or board[i-k][j+k] == 'R' or board[i-k][j+k] == 'B' or board[i-k][j+k] == 'N':
                                        if k != 0:
 
                                            queen_pairs.append((i,j,i-k,j+k))
                                            h += 1
                                            booooo = False
                                    elif board[i-k][j+k] == '1':
                                        continue   
                                    else:
                                            
                                        booooo = False
                                            
                    else:
                        break
                
                
                
                
                
                
                
                    
            if (i,j) in my_lst[0]:
                if j - 1 >= 0 and 0 <= i<row and board[i][j-1] != 'x':
                    if board[i][j-1] != '1' and not (i,j,i,j-1) in king_pairs:
                        king_pairs.append((i,j,i,j-1))
                        h += 1
                if j + 1 < col and 0<=i<row and board[i][j+1] != 'x':
                    if board[i][j+1] != '1' and not (i,j,i,j+1) in king_pairs:
                        king_pairs.append((i,j,i,j+1))
                        h += 1
                if i - 1 >= 0 and 0<=j<col and board[i-1][j] != 'x':
                    if board[i-1][j] != '1' and not (i,j,i-1,j) in king_pairs:
                        king_pairs.append((i,j,i-1,j))
                        h += 1 
                if i + 1 < row and 0<=j<col and board[i+1][j] != 'x':
                    if board[i+1][j] != '1' and not (i,j,i+1,j) in king_pairs:
                        king_pairs.append((i,j,i+1,j))
                        h += 1 
                if j - 1 >= 0 and i - 1 >= 0 and board[i-1][j-1] != 'x':
                    if board[i-1][j-1] != '1' and not (i,j,i-1,j-1) in king_pairs:
                        king_pairs.append((i,j,i-1,j-1))
                        h += 1
                if j + 1 < col and i - 1 >= 0 and board[i-1][j+1] != 'x':
                    if board[i-1][j+1] != '1' and not (i,j,i-1,j+1) in king_pairs:
                        king_pairs.append((i,j,i-1,j+1))
                        h += 1
                if j - 1 >= 0 and i + 1 < row and board[i+1][j-1] != 'x':
                    if board[i+1][j-1] != '1' and not (i,j,i+1,j-1) in king_pairs:
                        king_pairs.append((i,j,i+1,j-1))
                        h += 1
                if j + 1 < col and i + 1 < row and board[i+1][j+1] != 'x':
                    if board[i+1][j+1] != '1' and not (i,j,i+1,j+1) in king_pairs:
                        king_pairs.append((i,j,i+1,j+1))
                        h += 1
                
                        
            if (i,j) in my_lst[2]:
                
                for k in range (1,j+1):
                    if 0 <= j-k < len(board[i]) and 0 <= i < row:
                        if board[i][j-k] == 'K' or board[i][j-k] == 'Q' or board[i][j-k] == 'R' or board[i][j-k] == 'B' or board[i][j-k] == 'N':
                            rook_pairs.append((i,j,i,j-k))
                            h += 1
                            break    
                        elif board[i][j-k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                
                
                        
                for k in range (1,col-j):
                    
                    if len(board[i]) > j+k >= 0 and 0 <= i < row:
                        if board[i][j+k] == 'K' or board[i][j+k] == 'Q' or board[i][j+k] == 'R' or board[i][j+k] == 'B' or board[i][j+k] == 'N':
                            rook_pairs.append((i,j,i,j+k))
                            h += 1
                            break
                        elif board[i][j+k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                
                        
                for k in range (1,row-i):
                    if 0<= i+k < row and 0<= j < len(board[i+k]):
                        if board[i+k][j] == 'K' or board[i+k][j] == 'Q' or board[i+k][j] == 'R' or board[i+k][j] == 'B' or board[i+k][j] == 'N':
                            rook_pairs.append((i,j,i+k,j))
                            h += 1
                            break
                        elif board[i+k][j] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                
                    
                        
                for k in range (1,i+1):
                    if row > i-k >= 0 and 0<= j < len(board[i-k]):
                        if board[i-k][j] == 'K' or board[i-k][j] == 'Q' or board[i-k][j] == 'R' or board[i-k][j] == 'B' or board[i-k][j] == 'N':
                            rook_pairs.append((i,j,i-k,j))
                            h += 1
                            break
                        elif board[i-k][j] == '1':
                            continue
                            
                        else:
                            break
                    else:
                        break
                
            
                    
            if (i,j) in my_lst[3]:
                
                boo = True
                for k in range(row-i +1):
                    
                    if boo == True:
                        for q in range(col-j +1):
                            
                            if k == q:
                                
                                if i+k < row and j+k < col:
                                    
                                    if board[i+k][j+k] == 'K' or board[i+k][j+k] == 'Q' or board[i+k][j+k] == 'R' or board[i+k][j+k] == 'B' or board[i+k][j+k] == 'N':
                                        if k != 0:
                                        
                                            bishop_pairs.append((i,j,i+k,j+k))
                                            
                                            h += 1
                                            boo = False
                                    elif board[i+k][j+k] == '1':
                                        continue
        
                                    else:
                                            
                                        boo = False
                                            
                    else:
                        break
               
                booo = True
                for k in range(i +1):
                    if booo == True:
                        for q in range(j +1):
                            if k == q:
                                if i-k >= 0 and j-k >= 0:
                                    if board[i-k][j-k] == 'K' or board[i-k][j-k] == 'Q' or board[i-k][j-k] == 'R' or board[i-k][j-k] == 'B' or board[i-k][j-k] == 'N':
                                        if k!= 0:
                                            bishop_pairs.append((i,j,i-k,j-k))
                                            h += 1
                                            booo = False
                                    elif board[i-k][j-k] == '1':
                                        continue       
                                    else:
                                            
                                        booo = False
                                            
                    else:
                        break
                
                    
                boooo = True           
                for k in range(row-i +1):
                    
                    if boooo == True:
                        for q in range(j+1):
                            if k == q:
                                if i+k < row and j-k >= 0:
                                    if board[i+k][j-k] == 'K' or board[i+k][j-k] == 'Q' or board[i+k][j-k] == 'R' or board[i+k][j-k] == 'B' or board[i+k][j-k] == 'N':
                                        if k != 0:
                                            
                                            bishop_pairs.append((i,j,i+k,j-k))
                                            h += 1
                                            boooo = False
                                        
                                    elif board[i+k][j-k] == '1':
                                        continue
                                    else:
                                            
                                        boooo = False
                                            
                    else:
                        break
                
                booooo = True           
                for k in range(i+1):
                        
                    if booooo == True:
                        for q in range((col-j)+1):
                            if k == q:
                                if i-k >= 0 and j+k < col:
                                    if board[i-k][j+k] == 'K' or board[i-k][j+k] == 'Q' or board[i-k][j+k] == 'R' or board[i-k][j+k] == 'B' or board[i-k][j+k] == 'N':
                                        if k != 0:
 
                                            bishop_pairs.append((i,j,i-k,j+k))
                                            h += 1
                                            booooo = False
                                    elif board[i-k][j+k] == '1':
                                        continue   
                                    else:
                                            
                                        booooo = False
                                            
                    else:
                        break
                
                
                        
                    
                         
                
 
            if (i,j) in my_lst[4]:
                if j + 1 < col and i + 2 < row and board[i+2][j+1] != 'x':
                    if board[i+2][j+1] != '1' and not (i,j,i+2,j+1) in knight_pairs:
                        knight_pairs.append((i,j,i+2,j+1))
                        h += 1
                        #print("q")
                if j - 1 >= 0 and i + 2 < row and board[i+2][j-1] != 'x':
                    if board[i+2][j-1] != '1' and not (i,j,i+2,j-1) in knight_pairs:
                        knight_pairs.append((i,j,i+2,j-1))
                        h += 1
                        #print("w")
                if j + 2 < col and i + 1 < row and board[i+1][j+2] != 'x':
                    if board[i+1][j+2] != '1' and not (i,j,i+1,j+2) in knight_pairs:
                        knight_pairs.append((i,j,i+1,j+2))
                        h += 1
                        #print("e")
                if j - 2 >= 0 and i + 1 < row and board[i+1][j-2] != 'x':
                    if board[i+1][j-2] != '1' and not (i,j,i+1,j-2) in knight_pairs:
                        knight_pairs.append((i,j,i+1,j-2))
                        h += 1
                        #print("r")
                if j - 1 >= 0 and i - 2 >= 0 and board[i-2][j-1] != 'x':
                    if board[i-2][j-1] != '1' and not (i,j,i-2,j-1) in knight_pairs:
                        knight_pairs.append((i,j,i-2,j-1))
                        h += 1
                        #print("y")
                if j + 1 < col and i - 2 >= 0 and board[i-2][j+1] != 'x':
                    if board[i-2][j+1] != '1' and not (i,j,i-2,j+1) in knight_pairs:
                        knight_pairs.append((i,j,i-2,j+1))
                        h += 1
                        #print("u")
                if j + 2 < col and i - 1 >= 0 and board[i-1][j+2] != 'x':
                    if board[i-1][j+2] != '1' and not (i,j,i-1,j+2) in knight_pairs:
                        knight_pairs.append((i,j,i-2,j+2))
                        h += 1
                        #print("i")
                if j - 2 >= 0 and i - 1 >= 0 and board[i-1][j-2] != 'x':
                    if board[i-1][j-2] != '1' and not (i,j,i-1,j-2) in knight_pairs:
                        knight_pairs.append((i,j,i-1,j-2))
                        h += 1
                        #print("o")
    
    return h
def min_neighbour(board,row,col,my_ll,my_h,D,E): #return the gameboard with 1 less piece and least h
    lower_list = []
    equal_list = []
    higher_list = []
    ll_index = 0
    for piece_type in my_ll:
        for piece in piece_type:
            randomness = random.random()
            if randomness < D/E:#0.9:
                piece_row = piece[0]
                piece_col = piece[1]
                bod = copy.deepcopy(board)
                bod[piece_row][piece_col] = '1'
                ll = copy.deepcopy(my_ll)
                ll[ll_index].remove(piece)
                cost = heuristic_value(bod,row,col,ll)
                if cost == 0:
                    return "found"
                if cost < my_h:
                    lower_list.append((cost,bod, ll))
                elif cost == my_h:
                    equal_list.append((cost, bod, ll))
                else:
                    higher_list.append((cost, bod, ll))
        ll_index += 1

            
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
    file = "allrook.txt"
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
    coor = [set(),set(),set(),set(),set()]
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
                    coor[0].add((y,x))
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
                    coor[1].add((y,x))
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
                    coor[2].add((y,x))
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
                    coor[3].add((y,x))
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
                    coor[4].add((y,x))
                    game_board[y][x] = 'N'
 #row by col y by x
    #hill climb
    KK = num_of_enemy
    current = copy.deepcopy(game_board)
    cor = copy.deepcopy(coor)
    
    
    
    while KK >= K_value:
        
        value_now = heuristic_value(current,rows,cols,cor)
        
        if value_now == 0:
            
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
                        
            randomm = random.choice(range(K_value,K_value+2))
            coor = [set(),set(),set(),set(),set()]
            
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
                            coor[0].add((y,x))
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
                            coor[1].add((y,x))
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
                            coor[2].add((y,x))
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
                            coor[3].add((y,x))
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
                            coor[4].add((y,x))
                            game_board[y][x] = 'N'
                
            KK = len(coor[0]) + len(coor[1]) +len(coor[2]) +len(coor[3]) +len(coor[4]) 
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
                coor = [set(),set(),set(),set(),set()]
                
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
                                coor[0].add((y,x))
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
                                coor[1].add((y,x))
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
                                coor[2].add((y,x))
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
                                coor[3].add((y,x))
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
                                coor[4].add((y,x))
                                game_board[y][x] = 'N'
                    
                KK = len(coor[0]) + len(coor[1]) +len(coor[2]) +len(coor[3]) +len(coor[4]) 
                current = game_board
                cor = coor
            # elif heuristic_value(succ,rows,cols,a) == 0:
            #     return(my_funcc(a))
               
                    
                    
       
    
 
print(run_local())
#run_local()                
'''
python /Users/lockmeilin/Downloads/CS3/Project\ 2/Local.py /Users/lockmeilin/Downloads/CS3/Project\ 2/Public\ Testcases/Local1.txt 

'''
