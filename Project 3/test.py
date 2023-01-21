# def byteToBinary(string):
#     return (bin(int(string, 16))[2:]).zfill(64)

# def printBoard(binary_string):
#     for i in range(8):
#         print(binary_string[i*8:(i+1)*8])

# printBoard(byteToBinary("0x000000000000FF00"))

from pickletools import uint8
import numpy as np
import copy

# print(np.uint64(0b11111000111110001111100011111000111110000000000000000000))


# to_change = np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000)
# for x in range (5):
#     for y in range(5):
#         copy_new = copy.copy(to_change)
#         copy_new = np.uint64(copy_new) >> np.uint64(y+8*(x))
#         print(copy_new)


o = np.uint8(0)

print('{:08b}'.format(o))

