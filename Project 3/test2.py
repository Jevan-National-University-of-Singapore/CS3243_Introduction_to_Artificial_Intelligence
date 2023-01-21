import numpy as np

# U64 arrPieceAttacks[6][64];
# U64 arrBlockersAndBeyond[6][64];
# U64 arrBehind[64][64];

# U64 pieceAttacks(int pc, int f, U64 occupied) {
#    assert(pc != piece::PAWN);

#    U64 ts = arrPieceAttacks[pc][f];
#    for (U64 b = occupied & arrBlockersAndBeyond[pc][f]; b != 0; b &= (b - 1)) {
#       int sq = bitScanForward(b);
#       ts &= ~arrBehind[f][sq];
#    }
#    return ts;
# } 

print(np.uint64(0b1111100011111000111110001111100011111000000000000000000000000000))

# 11111000
# 11111000
# 11111000
# 11111000
# 11111000
# 00000000
# 00000000
# 00000000

# def pieceAttacks(column, occupied):
#     ts = uint64()