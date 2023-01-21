import sys
 
def splitt(word):
    head = word.rstrip('0123456789')
    tail = word[len(head):]
    lst = [head,tail]
    return(lst)
def my_func(path):
    my_ans = []
    for i in range(len(path)):
        if i != len(path) - 1:
            my_ans.append([path[i],path[i+1]])
    return(my_ans)
 
    
 
    
        
    
 
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    file = sys.argv[1]
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
    counter = 0
 
    # You can code in here but you cannot remove this function or change the return type
    #with open("Public Testcases/1.txt",'r') as data_file:
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
                for a in data[1].strip().split(' '):
                    pos_obs.append(a)
                    
            elif data[0] == "Number of Enemy King, Queen, Bishop, Rook, Knight (space between)":
                list_of_enemies = data[1].strip().split(' ')
                num_of_enemy_kings = int(list_of_enemies[0])
                
            elif data[0] == "Number of Own King, Queen, Bishop, Rook, Knight (space between)":
                num_own = data[1]
    
            elif data[0] == "Goal Positions (space between)":
                goals = data[1].strip().split(' ')
    
            
            elif data[0].find('King') == True :
                
                if counter == num_of_enemy_kings:
                    
                    my_pos.extend(data[0].split())
                    
                    
                else:
                    counter = counter + 1
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
            else:
                step_costs.extend(data[0].split())
    data_file.close()
    
    game_board = [[1] * int(cols) for i in range(int(rows))]
 
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
                    game_board[y][x] = '2'
 #row by col y by x
                    if x - 1 >= 0:
                        game_board[y][x-1] = '2' 
                    if x + 1 < cols:
                        game_board[y][x+1] = '2'
                    if y - 1 >= 0:
                        game_board[y-1][x] = '2'
                    if y + 1 < rows:
                        game_board[y+1][x] = '2'
                    if x - 1 >= 0 and y - 1 >= 0:
                        game_board[y-1][x-1] = '2'
                    if x + 1 < cols and y - 1 >= 0:
                        game_board[y-1][x+1] = '2'
                    if x - 1 >= 0 and y + 1 < rows:
                        game_board[y+1][x-1] = '2'
                    if x + 1 < cols and y + 1 < rows:
                        game_board[y+1][x+1] = '2'
                        
        elif 'Queen' in enemy:
             
            temp = enemy.split(',')
            pos = temp[1]#e0
           
            x = splitt(pos)[0]#e
 
            if len(x) > 0:
 
                x = ord(x) - 97 #e = 4
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    game_board[y][x] = '2'
                    boo = True
                    for i in range(rows-y +1):
                        if boo == True:
                            for q in range(cols-x +1):
                                if i == q:
                                    if y+i < rows and x+q < cols:
                                        if game_board[y+i][x+q] != 'x':
                                        
                                            game_board[y+i][x+q] = '2'
                                        else:
                                            boo = False
                        else:
                            break
                    booo = True
                    for i in range(y +1):
                        if booo == True:
                            for q in range(x +1):
                                if i == q:
                                    if y-i >= 0 and x-q >= 0:
                                        if game_board[y-i][x-q] != 'x':
                                    
                                        
                                            game_board[y-i][x-q] = '2'
                                        else:
                                            booo = False
                        else:
                            break
                    boooo = True           
                    for i in range(rows-y +1):
                        if boooo == True:
                            for q in range(x+1):
                                if i == q:
                                    if y+i < rows and x-q >= 0:
                                        if game_board[y+i][x-q] != 'x':
                                    
                                        
                                            game_board[y+i][x-q] = '2'
                                        else:
                                            boooo = False
                        else:
                            break
                                
                                
                    booooo = True          
                    for i in range(y+1):
                        
                        if booooo == True:
                            for q in range((cols-x)+1):
                                if i == q:
                                    if y-i >= 0 and x+q < cols:
                                        if game_board[y-i][x+q] != 'x':
                                            
                                        
                                            game_board[y-i][x+q] = '2'
                                        else:
                                            booooo = False
                        else:
                            break
                    ##
                    for q in range (cols-x +1):
                        if game_board[y][x+q] != 'x':
                            if x+q < cols:
                                game_board[y][x+q] = '2'
                        else:
                            break
                        
                    for q in range (x+1):
                        if game_board[y][x-q] != 'x':
                            if x-q >= 0:
                                game_board[y][x-q] = '2'
                        else:
                            break
                        
                    for i in range (rows-y +1):
                        if game_board[y+i][x] != 'x':
                            if y+i < rows:
                                game_board[y+i][x] = '2'
                        else:
                            break
                        
                    for i in range (y+1):
                        if game_board[y-i][x] != 'x':
                            if y-i >= 0:
                                game_board[y-i][x] = '2'
                        else:
                            break
                    

                    
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
                    
                    game_board[y][x] = '2'
 #row by col y by x
                    boo = True
                    for i in range(rows-y +1):
                        if boo == True:
                            for q in range(cols-x +1):
                                if i == q:
                                    if y+i < rows and x+q < cols:
                                        if game_board[y+i][x+q] != 'x':
                                        
                                            game_board[y+i][x+q] = '2'
                                        else:
                                            
                                            boo = False
                                            
                        else:
                            break
                    booo = True
                    for i in range(y +1):
                        if booo == True:
                            for q in range(x +1):
                                if i == q:
                                    if y-i >= 0 and x-q >= 0:
                                        if game_board[y-i][x-q] != 'x':
                                    
                                        
                                            game_board[y-i][x-q] = '2'
                                        else:
                                            
                                            booo = False
                                            
                        else:
                            break
                        
                    boooo = True           
                    for i in range(rows-y +1):
                        if boooo == True:
                            for q in range(x+1):
                                if i == q:
                                    if y+i < rows and x-q >= 0:
                                        if game_board[y+i][x-q] != 'x':
                                    
                                        
                                            game_board[y+i][x-q] = '2'
                                        else:
                                            
                                            boooo = False
                                            
                        else:
                            break
                                
                                
                    booooo = True           
                    for i in range(y+1):
                        
                        if booooo == True:
                            for q in range((cols-x)+1):
                                if i == q:
                                    if y-i >= 0 and x+q < cols:
                                        if game_board[y-i][x+q] != 'x':
                                            
                                        
                                            game_board[y-i][x+q] = '2'
                                        else:
                                            
                                            booooo = False
                                            
                        else:
                            break
                                        
                    
                                
        elif 'Rook' in enemy:
            temp = enemy.split(',')
            pos = temp[1]#e0
            x = splitt(pos)[0]#e
 
            if len(x) > 0:
 
                x = ord(x) - 97 #e = 4
                y = splitt(pos)[1]
 
                if len(y) > 0:
 
                    y = int(y)
                    x = int(x)
                    game_board[y][x] = '2'
 #row by col y by x
                    for q in range (cols-x +1):
                        if x+q < cols:
                            if game_board[y][x+q] != 'x':
                            
                                game_board[y][x+q] = '2'
                            else:
                                break
                        
                    for q in range (x+1):
                        if x-q >= 0:
                            if game_board[y][x-q] != 'x':
                            
                                game_board[y][x-q] = '2'
                            else:
                                break
                        
                    for i in range (rows-y +1):
                        if y+i < rows:
                            if game_board[y+i][x] != 'x':
                            
                                game_board[y+i][x] = '2'
                            else:
                                break
                        
                    for i in range (y+1):
                        if y-i >= 0:
                            if game_board[y-i][x] != 'x':
                            
                                game_board[y-i][x] = '2'
                            else:
                                break
                            
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
                    game_board[y][x] = '2'
 #row by col y by x
                
                    if x + 1 < cols and y + 2 < rows:
                        game_board[y+2][x+1] = '2'
                    if x - 1 >= 0 and y + 2 < rows:
                        game_board[y+2][x-1] = '2'
                    if x + 2 < cols and y + 1 < rows:
                        game_board[y+1][x+2] = '2'
                    if x - 2 >= 0 and y + 1 < rows:
                        game_board[y+1][x-2] = '2'
                    if x + 1 < cols and y - 2 >= 0:
                        game_board[y-2][x+1] = '2'
                    if x - 1 >= 0 and y - 2 >= 0:
                        game_board[y-2][x-1] = '2'
                    if x + 1 < cols and y - 2 >= 0:
                        game_board[y-2][x+1] = '2'
                    if x + 2 < cols and y - 1 >= 0:
                        game_board[y-1][x+2] = '2'
                    if x - 2 >= 0 and y - 1 >= 0:
                        game_board[y-1][x-2] = '2'
        
        
    start = 0
    
    for pos in my_pos:
        
        pos = pos[1 : : ]
        pos = pos[ :-1: ]
        start = pos
    
    temp = start.split(',')
    coor = temp[1]    
    my_x = 0
    my_y = 0
        
        
    coor = temp[1]#e5
    my_x = splitt(coor)[0]#e
    my_y = int(splitt(coor)[1])#y=5
    my_tup = (my_x,my_y)#(e,5)
 
    my_xx = ord(my_x) - 97
    game_board[my_y][my_xx] = 1
    print(game_board)
    #BFS
    q = []
    q.append([my_tup])
    
    visited_set = []
  
    while len(q) != 0:
        
            
        current = q.pop()#[('a',0)]
        
        y = current[len(current)-1][1]#0
        x = current[len(current)-1][0]#0
        
        if len(x) > 0:
            x = ord(x) - 97#x=e=4
            x = int(x)
        
        #append into q all the valid next moves from current[0]
        
            
        if (y,x) not in visited_set and game_board[y][x] != 'x' and game_board[y][x] != '2':
            
            
            for i in range(len(goals)):#check if (y,x) is a goal
                goal_X =splitt(goals[i])[0]
                goal_X =ord(goal_X) - 97
                
                goal_Y =splitt(goals[i])[1]
                goal_coor = (int(goal_Y),goal_X)
                game_board[int(goal_Y)][goal_X] = 1
                if str(tuple([y,x])) == str(goal_coor):
                    
                    
                    return my_func(current), len(visited_set)
                
            
            visited_set.append((y,x))
            
        
            
            
            if x-1 >= 0 and game_board[y][x-1] != 'x' and game_board[y][x-1] != '2' and (y,x-1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97-1),y)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("1")
                #print(current)
                
            
            if x+1 < cols and game_board[y][x+1] != 'x' and game_board[y][x+1] != '2' and (y,x+1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97+1),y)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("2")
                #print(current) 
            if y-1 >= 0 and game_board[y-1][x] != 'x' and game_board[y-1][x] != '2' and(y-1,x) not in visited_set:
                path = current.copy()
                poss = (chr(x+97),y-1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("3")
                #print(current)
 
            if y+1 < rows and game_board[y+1][x] != 'x' and game_board[y+1][x] != '2' and (y+1,x) not in visited_set:
                path = current.copy()
                poss = (chr(x+97),y+1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("4")
                #print(current)
 
            if x - 1 >= 0 and y - 1 >= 0 and game_board[y-1][x-1] != 'x' and game_board[y-1][x-1] != '2' and (y-1,x-1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97-1),y-1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("5")
                #print(current)
 
            if x + 1 < cols and y - 1 >= 0 and game_board[y-1][x+1] != 'x' and game_board[y-1][x+1] != '2' and (y-1,x+1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97+1),y-1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("6")
                #print(current)
 
            if x - 1 >= 0 and y + 1 < rows and game_board[y+1][x-1] != 'x' and game_board[y+1][x-1] != '2' and (y+1,x-1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97-1),y+1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("7")
                #print(current)
 
            if x + 1 < cols and y + 1 < rows and game_board[y+1][x+1] != 'x' and game_board[y+1][x+1] != '2' and (y+1,x+1) not in visited_set:
                path = current.copy()
                poss = (chr(x+97+1),y+1)
                path.append(poss)
                q.append(path)
                #print(path)
                #print(poss)
                #print("8")
                #print(current)
            
   
    
    
                
    return [], len(visited_set)
                    
                
           
print(run_BFS())
 
                
            
        
                       
                
                 
                
                  
                  
              
                
                    
        #if current.left is not None: q.append(current.left)
        #if current.right is not None: q.append(current.right)
            
   
        
  
    #moves, nodesExplored = search() #For reference
    #return moves, nodesExplored #Format to be returned
        
 
     
 
 
    

