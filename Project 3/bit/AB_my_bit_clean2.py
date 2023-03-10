

##=================== GLOBAL VARIABLES START ==================             ####T_GBL
from collections import deque
from operator import xor
import numpy as np
import copy

KNIGHTS_MOVES = {
    9223372036854775808 : 9077567998918656,
    4611686018427387904 : 4679521487814656,
    2305843009213693952 : 38368557762871296,
    1152921504606846976 : 18058378974593024,
    576460752303423488  : 9024791440785408,

    36028797018963968   : 2305878468463689728,
    18014398509481984   : 1152939783987658752,
    9007199254740992    : 9799982666336960512,
    4503599627370496    : 4611756558970257408,
    2251799813685248    : 2305878262305259520,

    140737488355328     : 4620693356194824192,
    70368744177664      : 11533718717099671552,
    35184372088832      : 5802888705324613632,
    17592186044416      : 2900318435575595008,
    8796093022208       : 1161928841568976896,

    549755813888        : 18049583418441728,
    274877906944        : 45053588728184832,
    137438953472        : 22667533999931392,
    68719476736         : 11329368886345728,
    34359738368         : 4538784536330240,

    2147483648          : 70506183131136,
    1073741824          : 175990579920896,
    536870912           : 88545045774336,
    268435456           : 44255343017984,
    134217728           : 17729624997888
}


SOUTH_ATTACK = {
    134217728: 0,                                  268435456: 0,                            536870912: 0,                                1073741824: 0,                               2147483648: 0,
    34359738368: 134217728,                          68719476736: 268435456,                  137438953472: 536870912,                     274877906944: 1073741824,                    549755813888: 2147483648, 
    8796093022208: 34493956096,                      17592186044416: 68987912192,             35184372088832: 137975824384,                70368744177664: 275951648768,                140737488355328: 551903297536, 
    2251799813685248: 8830586978304,                 4503599627370496: 17661173956608,        9007199254740992: 35322347913216,            18014398509481984: 70644695826432,           36028797018963968: 141289391652864, 
    576460752303423488: 2260630400663552,            1152921504606846976: 4521260801327104,   2305843009213693952: 9042521602654208,       4611686018427387904: 18085043205308416,      9223372036854775808: 36170086410616832
}

NORTH_ATTACK = {
    134217728: 578721382569869312,                 268435456: 1157442765139738624,          536870912: 2314885530279477248,              1073741824: 4629771060558954496,             2147483648: 9259542121117908992,
    34359738368: 578721348210130944,                 68719476736: 1157442696420261888,        137438953472: 2314885392840523776,           274877906944: 4629770785681047552,           549755813888: 9259541571362095104,
    8796093022208: 578712552117108736,               17592186044416: 1157425104234217472,     35184372088832: 2314850208468434944,         70368744177664: 4629700416936869888,         140737488355328: 9259400833873739776,
    2251799813685248: 576460752303423488,            4503599627370496: 1152921504606846976,   9007199254740992: 2305843009213693952,       18014398509481984: 4611686018427387904,      36028797018963968: 9223372036854775808,
    576460752303423488: 0,                           1152921504606846976: 0,                  2305843009213693952: 0,                      4611686018427387904: 0,                      9223372036854775808: 0
}

WEST_ATTACK = {
    134217728: 4026531840,                     268435456: 3758096384,                        536870912: 3221225472,                      1073741824: 2147483648,                      2147483648: 0,                      
    34359738368: 1030792151040,                  68719476736: 962072674304,                    137438953472: 824633720832,                 274877906944: 549755813888,                  549755813888: 0,                      
    8796093022208: 263882790666240,              17592186044416: 246290604621824,              35184372088832: 211106232532992,            70368744177664: 140737488355328,             140737488355328: 0,
    2251799813685248: 67553994410557440,         4503599627370496: 63050394783186944,          9007199254740992: 54043195528445952,        18014398509481984: 36028797018963968,        36028797018963968: 0,
    576460752303423488: 17293822569102704640,    1152921504606846976: 16140901064495857664,    2305843009213693952: 13835058055282163712,  4611686018427387904: 9223372036854775808,    9223372036854775808: 0
}

EAST_ATTACK = {
    134217728: 0,                               268435456: 134217728,                       536870912: 402653184,                        1073741824: 939524096,                       2147483648: 2013265920,
    34359738368: 0,                               68719476736: 34359738368,                   137438953472: 103079215104,                  274877906944: 240518168576,                  549755813888: 515396075520,
    8796093022208: 0,                             17592186044416: 8796093022208,              35184372088832: 26388279066624,              70368744177664: 61572651155456,              140737488355328: 131941395333120,
    2251799813685248: 0,                          4503599627370496: 2251799813685248,         9007199254740992: 6755399441055744,          18014398509481984: 15762598695796736,        36028797018963968: 33776997205278720,
    576460752303423488: 0,                        1152921504606846976: 576460752303423488,    2305843009213693952: 1729382256910270464,    4611686018427387904: 4035225266123964416,    9223372036854775808: 8646911284551352320 
}

NORTHEAST_ATTACK = {
    134217728: 0,                              268435456: 34359738368,                      536870912: 8864812498944,                    1073741824: 2269529438683136,                2147483648: 580999811180789760,
    34359738368: 0,                              68719476736: 8796093022208,                  137438953472: 2269391999729664,              274877906944: 580999536302882816,            549755813888: 1161999072605765632,
    8796093022208: 0,                            17592186044416: 2251799813685248,            35184372088832: 580964351930793984,          70368744177664: 1161928703861587968,         140737488355328: 2323857407723175936, 
    2251799813685248: 0,                         4503599627370496: 576460752303423488,        9007199254740992: 1152921504606846976,       18014398509481984: 2305843009213693952,      36028797018963968: 4611686018427387904, 
    576460752303423488: 0,                       1152921504606846976: 0,                      2305843009213693952: 0,                      4611686018427387904: 0,                      9223372036854775808: 0
}

NORTHWEST_ATTACK = {
    134217728: 9241421688455823360,              268435456: 36099303202095104,                  536870912: 141012366262272,                  1073741824: 549755813888,                    2147483648: 0,
    34359738368: 4620710809868173312,            68719476736: 9241421619736346624,            137438953472: 36099165763141632,             274877906944: 140737488355328,               549755813888: 0,
    8796093022208: 2310346608841064448,          17592186044416: 4620693217682128896,         35184372088832: 9241386435364257792,         70368744177664: 36028797018963968,           140737488355328: 0,
    2251799813685248: 1152921504606846976,       4503599627370496: 2305843009213693952,       9007199254740992: 4611686018427387904,       18014398509481984: 9223372036854775808,      36028797018963968: 0,
    576460752303423488: 0,                       1152921504606846976: 0,                      2305843009213693952:  0,                     4611686018427387904: 0,                      9223372036854775808: 0
}

SOUTHWEST_ATTACK = {
    134217728: 0,                                268435456: 0,                                  536870912: 0,                                1073741824: 0,                               536870912: 0, 
    34359738368: 268435456,                      68719476736: 536870912,                      137438953472: 1073741824,                    274877906944: 2147483648,                    549755813888: 0,
    8796093022208: 69256347648,                  17592186044416: 138512695296,                35184372088832: 277025390592,                70368744177664: 549755813888,                140737488355328: 0,
    2251799813685248: 17730698739712,            4503599627370496: 35461397479424,            9007199254740992: 70918499991552,            18014398509481984: 140737488355328,          36028797018963968: 0,
    576460752303423488: 4539061024849920,        1152921504606846976: 9078117754732544,       2305843009213693952: 18155135997837312,      4611686018427387904: 36028797018963968,      9223372036854775808: 0
}

SOUTHEAST_ATTACK ={
    134217728: 0,                                268435456: 0,                                  536870912: 0,                                1073741824: 0,                               2147483648: 0, 
    34359738368: 0,                              68719476736: 134217728,                      137438953472: 268435456,                     274877906944: 536870912,                     549755813888: 1073741824,
    8796093022208: 0,                            17592186044416: 34359738368,                 35184372088832: 68853694464,                 70368744177664: 137707388928,                140737488355328: 275414777856,
    2251799813685248: 0,                         4503599627370496: 8796093022208,             9007199254740992: 17626545782784,            18014398509481984: 35253225783296,           36028797018963968: 70506451566592,
    576460752303423488: 0,                       1152921504606846976: 2251799813685248,       2305843009213693952: 4512395720392704,       4611686018427387904: 9024825800523776,       9223372036854775808: 18049651735265280
}

SOUTH_ATTACK_BY_INDEX = {
    27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 35: 134217728, 36: 268435456, 37: 536870912, 38: 1073741824, 39: 2147483648, 43: 34493956096, 44: 68987912192, 45: 137975824384, 46: 275951648768, 47: 551903297536, 51: 8830586978304, 52: 17661173956608, 53: 35322347913216, 54: 70644695826432, 55: 141289391652864, 59: 2260630400663552, 60: 4521260801327104, 61: 9042521602654208, 62: 18085043205308416, 63: 36170086410616832
}

NORTH_ATTACK_BY_INDEX = {
    27: 578721382569869312, 28: 1157442765139738624, 29: 2314885530279477248, 30: 4629771060558954496, 31: 9259542121117908992, 35: 578721348210130944, 36: 1157442696420261888, 37: 2314885392840523776, 38: 4629770785681047552, 39: 9259541571362095104, 43: 578712552117108736, 44: 1157425104234217472, 45: 2314850208468434944, 46: 4629700416936869888, 47: 9259400833873739776, 51: 576460752303423488, 52: 1152921504606846976, 53: 2305843009213693952, 54: 4611686018427387904, 55: 9223372036854775808, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}

WEST_ATTACK_BY_INDEX = {
    27: 4026531840, 28: 3758096384, 29: 3221225472, 30: 2147483648, 31: 0, 35: 1030792151040, 36: 962072674304, 37: 824633720832, 38: 549755813888, 39: 0, 43: 263882790666240, 44: 246290604621824, 45: 211106232532992, 46: 
140737488355328, 47: 0, 51: 67553994410557440, 52: 63050394783186944, 53: 54043195528445952, 54: 36028797018963968, 55: 0, 59: 17293822569102704640, 60: 16140901064495857664, 61: 13835058055282163712, 62: 9223372036854775808, 63: 0
}

EAST_ATTACK_BY_INDEX = {
    27: 0, 28: 134217728, 29: 402653184, 30: 939524096, 31: 2013265920, 35: 0, 36: 34359738368, 37: 103079215104, 38: 240518168576, 39: 515396075520, 43: 0, 44: 8796093022208, 45: 26388279066624, 46: 61572651155456, 47: 131941395333120, 51: 0, 52: 2251799813685248, 53: 6755399441055744, 54: 15762598695796736, 55: 33776997205278720, 59: 0, 60: 576460752303423488, 61: 1729382256910270464, 62: 4035225266123964416, 63: 8646911284551352320 
}

NORTHEAST_ATTACK_BY_INDEX = {
    27: 0, 28: 34359738368, 29: 8864812498944, 30: 2269529438683136, 31: 580999811180789760, 35: 0, 36: 8796093022208, 37: 2269391999729664, 38: 580999536302882816, 39: 1161999072605765632, 43: 0, 44: 2251799813685248, 45: 580964351930793984, 46: 1161928703861587968, 47: 2323857407723175936, 51: 0, 52: 576460752303423488, 53: 1152921504606846976, 54: 2305843009213693952, 55: 4611686018427387904, 
    59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}

NORTHWEST_ATTACK_BY_INDEX = {
    27: 9241421688455823360, 28: 36099303202095104, 29: 141012366262272, 30: 549755813888, 31: 0, 35: 4620710809868173312, 36: 9241421619736346624, 37: 36099165763141632, 38: 140737488355328, 39: 0, 43: 2310346608841064448, 44: 4620693217682128896, 45: 9241386435364257792, 46: 36028797018963968, 47: 0, 51: 1152921504606846976, 52: 2305843009213693952, 53: 4611686018427387904, 54: 9223372036854775808, 55: 0, 
    59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}

SOUTHWEST_ATTACK_BY_INDEX = {
    27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 35: 268435456, 36: 536870912, 37: 1073741824, 38: 2147483648, 39: 0, 43: 69256347648, 44: 138512695296, 45: 277025390592, 46: 549755813888, 47: 0, 51: 17730698739712, 52: 35461397479424, 53: 70918499991552, 54: 140737488355328, 55: 0, 
    59: 4539061024849920, 60: 9078117754732544, 61: 18155135997837312, 62: 36028797018963968, 63: 0
}

SOUTHEAST_ATTACK_BY_INDEX ={
    27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 35: 0, 36: 134217728, 37: 268435456, 38: 536870912, 39: 1073741824, 43: 0, 44: 34359738368, 45: 68853694464, 46: 137707388928, 47: 275414777856, 51: 0, 52: 8796093022208, 53: 17626545782784, 54: 35253225783296, 55: 70506451566592, 
    59: 0, 60: 2251799813685248, 61: 4512395720392704, 62: 9024825800523776, 63: 18049651735265280
}

DEBRUJIN = np.uint64(0x03f79d71b4cb0a89)

LSB_DEBRUJIN = np.array(
        [ 0,  1, 48,  2, 57, 49, 28,  3,
         61, 58, 50, 42, 38, 29, 17,  4,
         62, 55, 59, 36, 53, 51, 43, 22,
         45, 39, 33, 30, 24, 18, 12,  5,
         63, 47, 56, 27, 60, 41, 37, 16,
         54, 35, 52, 21, 44, 32, 23, 11,
         46, 26, 40, 15, 34, 20, 31, 10,
         25, 14, 19,  9, 13,  8,  7,  6],
        dtype=np.uint8)

MSB_DEBRUJIN = np.array(
        [ 0, 47,  1, 56, 48, 27,  2, 60,
         57, 49, 41, 37, 28, 16,  3, 61,
         54, 58, 35, 52, 50, 42, 21, 44,
         38, 32, 29, 23, 17, 11,  4, 62,
         46, 55, 26, 59, 40, 36, 15, 53,
         34, 51, 20, 43, 31, 22, 10, 45,
         25, 39, 14, 33, 19, 30,  9, 24,
         13, 18,  8, 12,  7,  6,  5, 63],
        dtype=np.uint8)

stringToIndex = {
    'a0': 63, 'b0': 62, 'c0': 61, 'd0': 60, 'e0': 59, 'f0': 58, 'g0': 57, 'h0': 56,
    'a1': 55, 'b1': 54, 'c1': 53, 'd1': 52, 'e1': 51, 'f1': 50, 'g1': 49, 'h1': 48,
    'a2': 47, 'b2': 46, 'c2': 45, 'd2': 44, 'e2': 43, 'f2': 42, 'g2': 41, 'h2': 40,
    'a3': 39, 'b3': 38, 'c3': 37, 'd3': 36, 'e3': 35, 'f3': 34, 'g3': 33, 'h3': 32,
    'a4': 31, 'b4': 30, 'c4': 29, 'd4': 28, 'e4': 27, 'f4': 26, 'g4': 25, 'h4': 24,
    'a5': 23, 'b5': 22, 'c5': 21, 'd5': 20, 'e5': 19, 'f5': 18, 'g5': 17, 'h5': 16,
    'a6': 15, 'b6': 14, 'c6': 13, 'd6': 12, 'e6': 11, 'f6': 10, 'g6': 9, 'h6': 8,
    'a7': 7, 'b7': 6, 'c7': 5, 'd7': 4, 'e7': 3, 'f7': 2, 'g7': 1, 'h7': 0
}

def INT(character: str) -> int: ##converts alpabets to integers
    return ord(character)-97

def CHR(integer: int) -> str: ##converts integers to alphabets
    return chr(integer+97)


def checkWithinBoard(x, y):
    return 0 <= x <= 4 and 0 <= y<=4




# ----------------------
# BIT FUNCTIONS
# -------------------
def bitscan_forward(bitboard) -> int:
    return LSB_DEBRUJIN[((bitboard & -bitboard) * DEBRUJIN) >> np.uint8(58)]

def bitscan_reverse(bitboard: np.uint64) -> np.uint64 or int:
    bitboard |= bitboard >> np.uint8(1)
    bitboard |= bitboard >> np.uint8(2)
    bitboard |= bitboard >> np.uint8(4)
    bitboard |= bitboard >> np.uint8(8)
    bitboard |= bitboard >> np.uint8(16)
    bitboard |= bitboard >> np.uint8(32)
    return MSB_DEBRUJIN[(bitboard * DEBRUJIN) >> np.uint8(58)]

def set_bit(bitboard: np.uint64, bit: int) -> np.uint64:
    return np.uint64(bitboard | np.uint64(1) << np.uint64(bit))

def clear_bit(bitboard: np.uint64, bit: int or np.uint64) -> np.uint64:
    return bitboard & ~(np.uint64(1) << np.uint64(bit))

def set_bb_limit(bitboard):
    return bitboard & np.uint64(17940362863826698240)

##==================== GLOBAL FUNCTIONS END ====================
##========================= CLASSES START ======================================= ####T_CLASS


class Column:
    A = {0, 8, 16, 24, 32, 40, 48, 56}
    B = {1, 9, 17, 25, 33, 41, 49, 57}
    C = {2, 10, 18, 26, 34, 42, 50, 58}
    D = {3, 11, 19, 27, 35, 43, 51, 59}
    E = {4, 12, 20, 28, 36, 44, 52, 60}
    F = {5, 13, 21, 29, 37, 45, 53, 61}
    G = {6, 14, 22, 30, 38, 46, 54, 62}
    H = {7, 15, 23, 31, 39, 47, 55, 63}

    hexA = np.uint64(0x0101010101010101)
    hexB = np.uint64(0x0202020202020202)
    hexC = np.uint64(0x0404040404040404)
    hexD = np.uint64(0x0808080808080808)
    hexE = np.uint64(0x1010101010101010)
    hexF = np.uint64(0x2020202020202020)
    hexG = np.uint64(0x4040404040404040)
    hexH = np.uint64(0x8080808080808080)

    Columns = [A, B, C, D, E, F, G, H]



class Row:
    x1 = {0, 1, 2, 3, 4, 5, 6, 7}
    x2 = {8, 9, 10, 11, 12, 13, 14, 15}
    x3 = {16, 17, 18, 19, 20, 21, 22, 23}
    x4 = {24, 25, 26, 27, 28, 29, 30, 31}
    x5 = {32, 33, 34, 35, 36, 37, 38, 39}
    x6 = {40, 41, 42, 43, 44, 45, 46, 47}
    x7 = {48, 49, 50, 51, 52, 53, 54, 55}
    x8 = {56, 57, 58, 59, 60, 61, 62, 63}

    hex1 = np.uint64(0x00000000000000FF)
    hex2 = np.uint64(0x000000000000FF00)
    hex3 = np.uint64(0x0000000000FF0000)
    hex4 = np.uint64(0x00000000FF000000)
    hex5 = np.uint64(0x000000FF00000000)
    hex6 = np.uint64(0x0000FF0000000000)
    hex7 = np.uint64(0x00FF000000000000)
    hex8 = np.uint64(0xFF00000000000000)

    ranks = [x1, x2, x3, x4, x5, x6, x7, x8]
    #--------------- BOARD CLASS START ---------------              ####T_BOARD
class Board:
    def __init__(self, my_pieces, enemy_pieces):
        self.white_rook_bb = np.uint64()
        self.white_king_bb = np.uint64()
        self.white_bishop_bb = np.uint64()
        self.white_pawn_bb = np.uint64()
        self.white_knight_bb = np.uint64()
        self.white_queen_bb = np.uint64()

        # black piece groups
        self.black_rook_bb = np.uint64()
        self.black_king_bb = np.uint64()
        self.black_bishop_bb = np.uint64()
        self.black_pawn_bb = np.uint64()
        self.black_knight_bb = np.uint64()
        self.black_queen_bb = np.uint64()

    @property
    def white_pieces_bb(self):
        return self.white_rook_bb | self.white_king_bb | self.white_bishop_bb | self.white_pawn_bb | self.white_knight_bb | self.white_queen_bb

    @property
    def black_pieces_bb(self):
        return self.black_rook_bb | self.black_king_bb | self.black_bishop_bb | self.black_pawn_bb | self.black_knight_bb | self.black_queen_bb
    
    @property
    def all_pieces_bb(self):
        return self.white_pieces_bb | self.black_pieces_bb
    
    @property
    def white_pawn_attacks(self):
        west = (self.white_pawn_bb >> np.uint64(9)) & ~np.uint64(Column.hexH)
        east = (self.white_pawn_bb >> np.uint64(7)) & ~np.uint64(Column.hexA)
        return east | west

    @property
    def black_pawn_west_attacks(self):
        east = (self.black_pawn_bb << np.uint64(9)) & ~np.uint64(Column.hexA)
        west = (self.black_pawn_bb << np.uint64(7)) & ~np.uint64(Column.hexH)
        return east | west



    def getKnightMoves(self, index):
        pass

    def getWhiteRookMoves(self):
        attacking = self.white_rook_bb
        block = np.uint64(EAST_ATTACK[attacking]) & self.all_pieces_bb
        east = np.uint64(EAST_ATTACK[attacking]) if block == 0 else np.uint64(EAST_ATTACK[attacking]) ^ np.uint64(EAST_ATTACK_BY_INDEX[bitscan_reverse(block)])

        block = np.uint64(NORTH_ATTACK[attacking]) & self.all_pieces_bb
        north = np.uint64(NORTH_ATTACK[attacking]) if block == 0 else np.uint64(NORTH_ATTACK[attacking]) ^ np.uint64(NORTH_ATTACK_BY_INDEX[bitscan_forward(block)])

        block = np.uint64(WEST_ATTACK[attacking]) & self.all_pieces_bb
        west = np.uint64(WEST_ATTACK[attacking]) if block == 0 else np.uint64(WEST_ATTACK[attacking]) ^ np.uint64(WEST_ATTACK_BY_INDEX[bitscan_forward(block)])

        block = np.uint64(SOUTH_ATTACK[attacking]) & self.all_pieces_bb
        south = np.uint64(SOUTH_ATTACK[attacking]) if block == 0 else np.uint64(SOUTH_ATTACK[attacking]) ^ np.uint64(SOUTH_ATTACK_BY_INDEX[bitscan_reverse(block)])

        return (west | east |north |south) & ~self.white_pieces_bb



    
    #--------------- BOARD CLASS END ---------------


##========================== FUNCTIONS START ===========================   
def printBitboard(bitboard):
    board = '{:064b}'.format(bitboard)
    for i in range(8):
        print(board[i*8:(i+1)*8])
    print("--------------")


#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    pass    



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
    board = Board(None, None)
    # print(board.getState())
    for position, metadata in gameboard.items():
        position = position[0] + str(position[1])
        index = stringToIndex[position]
        piece_type = metadata[0]
        if metadata[1] == "White":
            if piece_type == "Queen":
                board.white_queen_bb = set_bit(board.white_queen_bb, index)
            elif piece_type == "King":
                board.white_king_bb = set_bit(board.white_king_bb, index)
            elif piece_type == "Bishop":
                board.white_bishop_bb = set_bit(board.white_bishop_bb, index)
            elif piece_type == "Rook":
                board.white_rook_bb = set_bit(board.white_rook_bb, index)
            elif piece_type == "Knight":
                board.white_knight_bb = set_bit(board.white_knight_bb, index)
            else:
                board.white_pawn_bb = set_bit(board.white_pawn_bb, index)
        else:
            if piece_type == "Queen":
                board.black_queen_bb = set_bit(board.black_queen_bb, index)
            elif piece_type == "King":
                board.black_king_bb = set_bit(board.black_king_bb, index)
            elif piece_type == "Bishop":
                board.black_bishop_bb = set_bit(board.black_bishop_bb, index)
            elif piece_type == "Rook":
                board.black_rook_bb = set_bit(board.black_rook_bb, index)
            elif piece_type == "Knight":
                board.black_knight_bb = set_bit(board.black_knight_bb, index)
            else:
                board.black_pawn_bb = set_bit(board.black_pawn_bb, index)

    # for row in range(27, 64, 8):
    #     for column in range(5):
    #         print(f"{row+column}: {set_bb_limit(southwestAttackBB(row+column))},", end = " ")
    # print("")

    printBitboard(board.getWhiteRookMoves())

    # printBitboard(board.getRookMoves(44, board))

    # printBitboard(NORTHWEST_ATTACK[43] & board.all_pieces_bb)

    # printBitboard(set_bb_limit(board.white_pawn_bb))



starting = {('a', 1): ('Pawn', 'White'), ('a', 3): ('Pawn', 'Black'), ('b', 1): ('Pawn', 'White'), ('b', 3): ('Pawn', 'Black'), ('c', 1): ('Pawn', 'White'), ('c', 3): ('Pawn', 'Black'),
('d', 1): ('Pawn', 'White'), ('d', 3): ('Pawn', 'Black'), ('e', 1): ('Pawn', 'White'), ('e', 3): ('Pawn', 'Black'), ('a', 0): ('Rook', 'White'), ('a', 4): ('Rook', 'Black'),
('b', 0): ('Knight', 'White'), ('b', 4): ('Knight', 'Black'), ('c', 0): ('Bishop', 'White'), ('c', 4): ('Bishop', 'Black'), ('d', 0): ('Queen', 'White'), ('d', 4): ('Queen', 'Black'), 
('e', 0): ('King', 'White'), ('e', 4): ('King', 'Black')}



print(studentAgent(starting))