import random

coor = {(1,2):"a", (5,2):"b", (10,3):"c", (80, 2):"d"}
enemies_pos_random = random.sample(list(coor),2)
print(enemies_pos_random)