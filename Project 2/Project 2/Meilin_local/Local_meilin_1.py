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
    for i in range(len(lst_of_lst)):
        for j in range(len(lst_of_lst[i])):
            if len(lst_of_lst[i]) != 0:
                
                y = lst_of_lst[i][j][0]
                x = lst_of_lst[i][j][1]
                   
                if i == 0:
                    my_ans[tuple((chr(x+97),y))] = 'King'
                        
                elif i == 1:
                    my_ans[tuple((chr(x+97),y))] = 'Queen'
                elif i == 2:
                    my_ans[tuple((chr(x+97),y))] = 'Rook'
                elif i == 3:
                    my_ans[tuple((chr(x+97),y))] = 'Bishop'
                elif i == 4:
                    my_ans[tuple((chr(x+97),y))] = 'Knight'
                    
            
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
                boo = True
                for k in range(row-i +1):
                    if boo == True:
                        for q in range(col-j +1):
                            if k == q:
                                if i+k < row and j+k < col:
                                    if board[i+k][j+k] != 'x' and board[i+k][j+k] != '1':
                                        if k != 0:
                                            
                                            queen_pairs.append((i,j,i+k,j+k))
                                            h += 1
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
                                    if board[i-k][j-k] != 'x' and board[i-k][j-k] != '1':
                                        if k != 0:
                                            queen_pairs.append((i,j,i-k,j-k))
                                            h += 1
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
                                    if board[i+k][j-k] != 'x' and board[i+k][j-k] != '1':
                                        if k != 0:
                                            queen_pairs.append((i,j,i+k,j-k))
                                            h += 1
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
                                    if board[i-k][j+k] != 'x' and board[i-k][j+k] != '1':
                                        if k != 0:
                                            queen_pairs.append((i,j,i-k,j+k))
                                            h += 1
                                    elif board[i-k][j+k] == '1':
                                        continue   
                                    else:
                                            
                                        booooo = False
                                            
                    else:
                        break
                    
                for k in range (1,(col-j)+1):
                    if 0 <= j+k < len(board[i]) and 0 <= i < row:
                        if board[i][j+k] != 'x' and board[i][j+k] != '1':
                            queen_pairs.append((i,j,i,j+k))
                            h += 1
                                
                        elif board[i][j+k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                for k in range (1,j+1):
                    if len(board[i]) > j-k >= 0 and 0 <= i < row:
                        if board[i][j-k] != 'x' and board[i][j-k] != '1':
                            queen_pairs.append((i,j,i,j-k))
                            h += 1
                        elif board[i][j-k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                    
                        
                for k in range (1,(row-i)+1):
                    if 0<= i+k < row and 0<= j < len(board[i+k]):
                        if board[i+k][j] != 'x' and board[i+k][j] != '1':
                            queen_pairs.append((i,j,i+k,j))
                            h += 1
                            
                        elif board[i+k][j] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                    
                        
                for k in range (1,i+1):
                    if row > i-k >= 0 and 0<= j < len(board[i-k]):
                        if board[i-k][j] != 'x' and board[i-k][j] != '1':
                            queen_pairs.append((i,j,i-k,j))
                            h += 1
                            
                        elif board[i-k][j] == '1':
                            continue
                            
                        else:
                            break
                    else:
                        break
                
                
                    
            if (i,j) in my_lst[0]:
                if j - 1 >= 0 and board[i][j-1] != 'x':
                    if board[i][j-1] != '1' and not (i,j,i,j-1) in king_pairs:
                        king_pairs.append((i, j, i, j-1))
                        h += 1       
                if j + 1 < col and board[i][j+1] != 'x':
                    if board[i][j+1] != '1' and not (i,j,i,j+1) in king_pairs:
                        king_pairs.append((i,j,i,j+1))
                        h += 1
                if i - 1 >= 0 and board[i-1][j] != 'x':
                    if board[i-1][j] != '1' and not (i,j,i-1,j) in king_pairs:
                        king_pairs.append((i,j,i-1,j))
                        h += 1 
                if i + 1 < row and board[i+1][j] != 'x':
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
                for k in range (1,(col-j)+1):
                    if 0 <= j+k < len(board[i]) and 0 <= i < row:
                        if board[i][j+k] != 'x' and board[i][j+k] != '1':
                            rook_pairs.append((i,j,i,j+k))
                            h += 1
                                
                        elif board[i][j+k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                for k in range (1,j+1):
                    if len(board[i]) > j-k >= 0 and 0 <= i < row:
                        if board[i][j-k] != 'x' and board[i][j-k] != '1':
                            rook_pairs.append((i,j,i,j-k))
                            h += 1
                        elif board[i][j-k] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                        
                    
                        
                for k in range (1,(row-i)+1):
                    if 0<= i+k < row and 0<= j < len(board[i+k]):
                        if board[i+k][j] != 'x' and board[i+k][j] != '1':
                            rook_pairs.append((i,j,i+k,j))
                            h += 1
                            
                        elif board[i+k][j] == '1':
                            continue
                        else:
                            break
                    else:
                        break
                    
                        
                for k in range (1,i+1):
                    if row > i-k >= 0 and 0<= j < len(board[i-k]):
                        if board[i-k][j] != 'x' and board[i-k][j] != '1':
                            rook_pairs.append((i,j,i-k,j))
                            h += 1
                            
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
                                    
                                    if board[i+k][j+k] != 'x' and board[i+k][j+k] != '1':
                                        if k != 0:
                                        
                                            bishop_pairs.append((i,j,i+k,j+k))
                                            
                                            h += 1
                                        
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
                                    if board[i-k][j-k] != 'x' and board[i-k][j-k] != '1':
                                        if k!= 0:
                                            bishop_pairs.append((i,j,i-k,j-k))
                                            h += 1
                                        
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
                                    if board[i+k][j-k] != 'x' and board[i+k][j-k] != '1':
                                        if k != 0:
                                            
                                            bishop_pairs.append((i,j,i+k,j-k))
                                            h += 1
                                        
                                        
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
                                    if board[i-k][j+k] != 'x' and board[i-k][j+k] != '1':
                                        if k != 0:
 
                                            bishop_pairs.append((i,j,i-k,j+k))
                                            h += 1
                                        
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
def min_neighbour(board,row,col,removed_piece_dict,my_ll,D,E,my_h_now): #return the gameboard with 1 less piece and least h
    queen_pairs = []
    king_pairs = []
    rook_pairs = []
    bishop_pairs = []
    knight_pairs = []
    less_than = []
    equal = []
    more_than =[]
  
    for i in range(row):
        for j in range(col):
            cost = 0
            
            if board[i][j] == 'K':
                randomness = random.random()
                if randomness < D/E:
                
                    if j - 1 >= 0 and board[i][j-1] != 'x':
                        if board[i][j-1] != '1' and not (i,j,i,j-1) in king_pairs:
                            king_pairs.append((i, j, i, j-1))
                            cost += 1       
                    if j + 1 < col and board[i][j+1] != 'x':
                        if board[i][j+1] != '1' and not (i,j,i,j+1) in king_pairs:
                            king_pairs.append((i,j,i,j+1))
                            cost += 1
                    if i - 1 >= 0 and board[i-1][j] != 'x':
                        if board[i-1][j] != '1' and not (i,j,i-1,j) in king_pairs:
                            king_pairs.append((i,j,i-1,j))
                            cost += 1 
                    if i + 1 < row and board[i+1][j] != 'x':
                        if board[i+1][j] != '1' and not (i,j,i+1,j) in king_pairs:
                            king_pairs.append((i,j,i+1,j))
                            cost += 1 
                    if j - 1 >= 0 and i - 1 >= 0 and board[i-1][j-1] != 'x':
                        if board[i-1][j-1] != '1' and not (i,j,i-1,j-1) in king_pairs:
                            king_pairs.append((i,j,i-1,j-1))
                            cost += 1
                    if j + 1 < col and i - 1 >= 0 and board[i-1][j+1] != 'x':
                        if board[i-1][j+1] != '1' and not (i,j,i-1,j+1) in king_pairs:
                            king_pairs.append((i,j,i-1,j+1))
                            cost += 1
                    if j - 1 >= 0 and i + 1 < row and board[i+1][j-1] != 'x':
                        if board[i+1][j-1] != '1' and not (i,j,i+1,j-1) in king_pairs:
                            king_pairs.append((i,j,i+1,j-1))
                            cost += 1
                    if j + 1 < col and i + 1 < row and board[i+1][j+1] != 'x':
                        if board[i+1][j+1] != '1' and not (i,j,i+1,j+1) in king_pairs:
                            king_pairs.append((i,j,i+1,j+1))
                            cost += 1
                        
                    if cost < my_h_now:
                        less_than.append((-cost,(i,j)))
                    if cost == my_h_now:
                        equal.append((-cost,(i,j)))
                    if cost < my_h_now:
                        more_than.append((-cost,(i,j)))
            
                       
                    
            elif board[i][j] == 'Q':
                randomness = random.random()
                if randomness < D/E:
                    boo = True
                    for k in range(row-i +1):
                        if boo == True:
                            for q in range(col-j +1):
                                if k == q:
                                    if i+k < row and j+k < col:
                                        if board[i+k][j+k] != 'x' and board[i+k][j+k] != '1':
                                            if k != 0:
                                                queen_pairs.append((i,j,i+k,j+k))
                                                cost += 1
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
                                        if board[i-k][j-k] != 'x' and board[i-k][j-k] != '1':
                                            if k != 0:
                                                queen_pairs.append((i,j,i-k,j-k))
                                                cost += 1
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
                                        if board[i+k][j-k] != 'x' and board[i+k][j-k] != '1':
                                            if k != 0:
                                                queen_pairs.append((i,j,i+k,j-k))
                                                cost += 1
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
                                        if board[i-k][j+k] != 'x' and board[i-k][j+k] != '1':
                                            if k != 0:
                                                queen_pairs.append((i,j,i-k,j+k))
                                                cost += 1
                                        elif board[i-k][j+k] == '1':
                                            continue   
                                        else:
                                                
                                            booooo = False
                                                
                        else:
                            break
                        
                    for k in range (1,(col-j)+1):
                        if 0 <= j+k < len(board[i]) and 0 <= i < row:
                            if board[i][j+k] != 'x' and board[i][j+k] != '1':
                                queen_pairs.append((i,j,i,j+k))
                                cost += 1
                                    
                            elif board[i][j+k] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                            
                    for k in range (1,j+1):
                        if len(board[i]) > j-k >= 0 and 0 <= i < row:
                            if board[i][j-k] != 'x' and board[i][j-k] != '1':
                                queen_pairs.append((i,j,i,j-k))
                                cost += 1
                            elif board[i][j-k] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                            
                        
                            
                    for k in range (1,(row-i)+1):
                        if 0<= i+k < row and 0<= j < len(board[i+k]):
                            if board[i+k][j] != 'x' and board[i+k][j] != '1':
                                queen_pairs.append((i,j,i+k,j))
                                cost += 1
                                
                            elif board[i+k][j] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                        
                            
                    for k in range (1,i+1):
                        if row > i-k >= 0 and 0<= j < len(board[i-k]):
                            if board[i-k][j] != 'x' and board[i-k][j] != '1':
                                queen_pairs.append((i,j,i-k,j))
                                cost += 1
                                
                            elif board[i-k][j] == '1':
                                continue
                                
                            else:
                                break
                        else:
                            break
                        
                    if cost < my_h_now:
                        less_than.append((-cost,(i,j)))
                    if cost == my_h_now:
                        equal.append((-cost,(i,j)))
                    if cost < my_h_now:
                        more_than.append((-cost,(i,j)))
           
                
            elif board[i][j] == 'R':
                randomness = random.random()
                if randomness < D/E:
                    for k in range (1,(col-j)+1):
                        if 0 <= j+k < len(board[i]) and 0 <= i < row:
                            if board[i][j+k] != 'x' and board[i][j+k] != '1':
                                rook_pairs.append((i,j,i,j+k))
                                cost += 1
                                    
                            elif board[i][j+k] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                            
                    for k in range (1,j+1):
                        if len(board[i]) > j-k >= 0 and 0 <= i < row:
                            if board[i][j-k] != 'x' and board[i][j-k] != '1':
                                rook_pairs.append((i,j,i,j-k))
                                cost += 1
                            elif board[i][j-k] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                            
                        
                            
                    for k in range (1,(row-i)+1):
                        if 0<= i+k < row and 0<= j < len(board[i+k]):
                            if board[i+k][j] != 'x' and board[i+k][j] != '1':
                                rook_pairs.append((i,j,i+k,j))
                                cost += 1
                                
                            elif board[i+k][j] == '1':
                                continue
                            else:
                                break
                        else:
                            break
                        
                            
                    for k in range (1,i+1):
                        if row > i-k >= 0 and 0<= j < len(board[i-k]):
                            if board[i-k][j] != 'x' and board[i-k][j] != '1':
                                rook_pairs.append((i,j,i-k,j))
                                cost += 1
                                
                            elif board[i-k][j] == '1':
                                continue
                                
                            else:
                                break
                        else:
                            break
                        
                    if cost < my_h_now:
                        less_than.append((-cost,(i,j)))
                    if cost == my_h_now:
                        equal.append((-cost,(i,j)))
                    if cost < my_h_now:
                        more_than.append((-cost,(i,j)))
           
                
            elif board[i][j] == 'B':
                randomness = random.random()
                if randomness < D/E:
                    boo = True
                    for k in range(row-i +1):
                        if boo == True:
                            for q in range(col-j +1):
                                if k == q:
                                    if i+k < row and j+k < col:
                                        if board[i+k][j+k] != 'x' and board[i+k][j+k] != '1':
                                            if k != 0:
                                                bishop_pairs.append((i,j,i+k,j+k))
                                                cost += 1
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
                                        if board[i-k][j-k] != 'x' and board[i-k][j-k] != '1':
                                            if k != 0:
                                                bishop_pairs.append((i,j,i-k,j-k))
                                                cost += 1
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
                                        if board[i+k][j-k] != 'x' and board[i+k][j-k] != '1':
                                            if k != 0:
                                                bishop_pairs.append((i,j,i+k,j-k))
                                                cost += 1
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
                                        if board[i-k][j+k] != 'x' and board[i-k][j+k] != '1':
                                            if k != 0:
                                                bishop_pairs.append((i,j,i-k,j+k))
                                                cost += 1
                                        elif board[i-k][j+k] == '1':
                                            continue   
                                        else:
                                                
                                            booooo = False
                                                
                        else:
                            break
                        
                    if cost < my_h_now:
                        less_than.append((-cost,(i,j)))
                    if cost == my_h_now:
                        equal.append((-cost,(i,j)))
                    if cost < my_h_now:
                        more_than.append((-cost,(i,j)))
                        
    
                    
                

            elif board[i][j] == 'N':
                randomness = random.random()
                if randomness < D/E:
                
                    if j + 1 < col and i + 2 < row and board[i+2][j+1] != 'x':
                        if board[i+2][j+1] != '1' and not (i,j,i+2,j+1) in knight_pairs:
                            knight_pairs.append((i,j,i+2,j+1))
                            cost += 1
                            #print("q")
                    if j - 1 >= 0 and i + 2 < row and board[i+2][j-1] != 'x':
                        if board[i+2][j-1] != '1' and not (i,j,i+2,j-1) in knight_pairs:
                            knight_pairs.append((i,j,i+2,j-1))
                            cost += 1
                            #print("w")
                    if j + 2 < col and i + 1 < row and board[i+1][j+2] != 'x':
                        if board[i+1][j+2] != '1' and not (i,j,i+1,j+2) in knight_pairs:
                            knight_pairs.append((i,j,i+1,j+2))
                            cost += 1
                            #print("e")
                    if j - 2 >= 0 and i + 1 < row and board[i+1][j-2] != 'x':
                        if board[i+1][j-2] != '1' and not (i,j,i+1,j-2) in knight_pairs:
                            knight_pairs.append((i,j,i+1,j-2))
                            cost += 1
                            #print("r")
                    if j - 1 >= 0 and i - 2 >= 0 and board[i-2][j-1] != 'x':
                        if board[i-2][j-1] != '1' and not (i,j,i-2,j-1) in knight_pairs:
                            knight_pairs.append((i,j,i-2,j-1))
                            cost += 1
                            #print("y")
                    if j + 1 < col and i - 2 >= 0 and board[i-2][j+1] != 'x':
                        if board[i-2][j+1] != '1' and not (i,j,i-2,j+1) in knight_pairs:
                            knight_pairs.append((i,j,i-2,j+1))
                            cost += 1
                            #print("u")
                    if j + 2 < col and i - 1 >= 0 and board[i-1][j+2] != 'x':
                        if board[i-1][j+2] != '1' and not (i,j,i-1,j+2) in knight_pairs:
                            knight_pairs.append((i,j,i-2,j+2))
                            cost += 1
                            #print("i")
                    if j - 2 >= 0 and i - 1 >= 0 and board[i-1][j-2] != 'x':
                        if board[i-1][j-2] != '1' and not (i,j,i-1,j-2) in knight_pairs:
                            knight_pairs.append((i,j,i-1,j-2))
                            cost += 1
                            #print("o")
                    if cost < my_h_now:
                        less_than.append((-cost,(i,j)))
                    if cost == my_h_now:
                        equal.append((-cost,(i,j)))
                    if cost < my_h_now:
                        more_than.append((-cost,(i,j)))
                            
                    
    b = (0,0)
    if less_than:
        heapq.heapify(less_than)
        b = heapq.heappop(less_than)[1]
        to_remove = b
    elif equal:
        heapq.heapify(equal)
        b = heapq.heappop(equal)[1]
        to_remove = b
    elif more_than and random.random() > D/E:
        heapq.heapify(more_than)
        b = heapq.heappop(less_than)[1]
        to_remove = b
        
        
    cop = copy.deepcopy(board)
    piece = cop[to_remove[0]][to_remove[1]]
    cop[to_remove[0]][to_remove[1]] = '1'
    hand = 0
    if piece == 'K':
        hand = 0
    if piece == 'Q':
        hand = 1
    if piece == 'R':
        hand = 2
    if piece == 'B':
        hand = 3
    if piece == 'N':
        hand = 4
        
    my_ll[hand].remove(to_remove)
    
    
    
    
    return cop                    
    
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)
 
# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    file = sys.argv[1] #Do not remove. This is your input testfile.
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
    coor = [[],[],[],[],[]]
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
                    coor[0].append((y,x))
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
                    coor[1].append((y,x))
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
                    coor[2].append((y,x))
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
                    coor[3].append((y,x))
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
                    coor[4].append((y,x))
                    game_board[y][x] = 'N'
 #row by col y by x
    #hill climb
    KK = num_of_enemy
    current = copy.deepcopy(game_board)
    cor = copy.deepcopy(coor)
   
    
    #print(coor)
    while KK >= K_value:
        
        value_now = heuristic_value(current,rows,cols,cor)
        num_pieces_now = len(cor)
        if value_now == 0:
            return my_funcc(cor)
        
        elif KK == K_value:
            KK = num_of_enemy
            current = copy.deepcopy(game_board)
            cor = copy.deepcopy(coor)
            #print("rr2")
            #print(cor)
            #print("rr2")
        else:
            q=[]
            heapq.heapify(q)
            KK -= 1
            neighbour = min_neighbour(current,rows,cols,q,cor,K_value,num_pieces_now,value_now)
            if heuristic_value(neighbour,rows,cols,cor) <= value_now:
                    
                        
                current = neighbour
                    
                    #print("...")
                    #print(KK)
                    #print(cor)
                    #print("...")
            else:
                
                
                KK = num_of_enemy
                current = copy.deepcopy(game_board)
                cor = copy.deepcopy(coor)
                
                
 
                    
                    
                
                    
                
                                
                
                
            
            
            
            
                
           
"""             
if heuristic_value(neighbour,rows,cols,cor) == 0:
                #print(my_funcc(a))
                #print(KK)
                #print(cor)
                return my_funcc(cor)
            
            else:
                if heuristic_value(neighbour,rows,cols,cor) <= value_now:
                    
                        
                    current = neighbour
                    
                    #print("...")
                    #print(KK)
                    #print(cor)
                    #print("...")
                else:
                    #print("Rr1")
                    KK = num_of_enemy
                    current = copy.deepcopy(game_board)
                    cor = copy.deepcopy(coor)
                    #print(cor)
                    #print("Rr1")
"""
print(run_local())
#run_local()        
