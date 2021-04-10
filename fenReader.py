# Takes in a FEN-string and returns a boardMatrix on the following format:
# (yes this convertion looses some information about the game that is not relevant for drawing the board)
# [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
#  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
#  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#  ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#  ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
def getBoardMatrix(fen):
    exception = Exception(f"FEN-string is not valid: {fen}")
    rows = fen.strip(" ").split(" ")[0].split("/")
    boardMatrix = []
    for row in rows:
        toAppend = []
        for char in row:
            if char in [str(n) for n in range(1, 9)]:
                toAppend += [" " for i in range(int(char))]
            elif char in ["r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"]:
                toAppend.append(char)
            else:
                raise exception
        if len(toAppend) != 8:
            raise exception
        boardMatrix.append(toAppend)
    if len(boardMatrix) != 8:
        raise exception
    return boardMatrix

# Takes in a FEN-string and returns:
# - "w" if white is in the move
# - "b" if black is in the move
def getPlayerInMove(fen):
    return fen.split(" ")[1].lower()
