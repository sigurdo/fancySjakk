import generalFunctions
import fenReader

# Arguments:
# - pieceType - color does not matter
# - toCol - one of "a", "b", "c", "d", "e", "f", "g", "h"
# - toRow - one of "1", "2", "3", "4", "5", "6", "7", "8"
# - fen - fen position of board before performing move
# - stockfish - stockfish.Stockfish instance
# - fromCol=0 - one of 0 (undefined), "1", "2", "3", "4", "5", "6", "7", "8"
# - fromRow=0 - one of 0 (undefined), "a", "b", "c", "d", "e", "f", "g", "h"
#
# Returns:
# - fromCol - one of "a", "b", "c", "d", "e", "f", "g", "h"
# - fromRow - one of "1", "2", "3", "4", "5", "6", "7", "8"
def findPieceTo(pieceType, toCol, toRow, fen, stockfish, fromCol=0, fromRow=0):
    boardMatrix = fenReader.getBoardMatrix(fen)
    player = fenReader.getPlayerInMove(fen)
    piece = pieceType.upper() if player == "w" else pieceType.lower()
    rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]

    possibleFroms = []
    for row in rows:
        if fromRow and fromRow != row: continue
        for col in cols:
            if fromCol and fromCol != col: continue
            rowNr = rows.index(row)
            colNr = cols.index(col)
            if (boardMatrix[rowNr][colNr] == piece):
                stockfish.set_fen_position(fen)
                # print(f"{col}{row}{toCol}{toRow}")
                if stockfish.is_move_correct(f"{col}{row}{toCol}{toRow}"):
                    possibleFroms.append((col, row))

    if (len(possibleFroms) > 1): raise Exception(f'Move is ambigous: {pieceType}{fromCol}{fromRow}{toCol}{toRow}')

    if (len(possibleFroms) < 1): raise Exception(f'Move is impossible: {pieceType}{fromCol}{fromRow}{toCol}{toRow}')

    return possibleFroms[0][0], possibleFroms[0][1]

# Arguments:
# - algebraic - algebraic notaion for the move, f ex "Rxd6"
# - fen - fen position of board before performing move
# - stockfish - stockfish.Stockfish instance
#
# Returns:
# - uci - uci notation for the move f ex "d3d6"
def algToUci(algebraic, fen, stockfish):
    if (" " in algebraic):
        raise Exception("Spaces not allowed in algebraic notaiton")

    pieceTypes = ["R", "N", "B", "Q", "K", "P"]
    colNames = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rowNames = [str(n) for n in range(1, 9)];
    promotionTypes = ["R", "N", "B", "Q", "P"]
    checkTypes = ["+", "#"]
    castlingTypes = ["0-0", "o-o", "O-O"]

    algebraic = f"{algebraic}_"
    move = {
        "pieceType": "P",
        "fromCol": 0,
        "fromRow": 0,
        "capture": 0,
        "toCol": 0,
        "toRow": 0,
        "promotion": 0,
        "check": 0,
    }
    i = 0

    if (algebraic[0:3] in castlingTypes):
        algebraic = algebraic.upper()
        algebraic = algebraic.replace("O", "0")
        move["pieceType"] = "K"
        move["fromRow"] = "1" if fenReader.getPlayerInMove(fen) == "w" else "8"
        move["toRow"] = move["fromRow"]
        move["fromCol"] = "e"
        move["toCol"] = "c" if algebraic[3] == "-" else "g"

    else:
        if (algebraic[i] in pieceTypes):
            move["pieceType"] = algebraic[i]
            i += 1

        fromSpecified = False
        j = i+1
        while (j < len(algebraic)):
            if (algebraic[j] in colNames):
                fromSpecified = True
                break
            j += 1

        if (fromSpecified):
            if (algebraic[i] in colNames and algebraic[i+1] in rowNames):
                move["fromCol"], move["fromRow"] = algebraic[i], algebraic[i+1]
                i += 2
            elif (algebraic[i] in colNames):
                move["fromCol"] = algebraic[i]
                i += 1
            elif (algebraic[i] in rowNames):
                move["fromRow"] = algebraic[i]
                i += 1

        if (algebraic[i] == "x"):
            move["capture"] = True
            i += 1
        else:
            move["capture"] = False

        if (algebraic[i] in colNames and algebraic[i+1] in rowNames): #Bare en dobbeltsjekk. Denne blokka bør kjøre uansett
            move["toCol"], move["toRow"] = algebraic[i], algebraic[i+1]
            i += 2

        if (algebraic[i] in promotionTypes):
            move["promotion"] = algebraic[i]
            i += 1
        elif (algebraic[i] == "=" and algebraic[i+1] in promotionTypes):
            move["promotion"] = algebraic[i+1]
            i += 2

        if (algebraic[i] in checkTypes):
            move["check"] = algebraic[i]
            i += 1

    move["fromCol"], move["fromRow"] = findPieceTo(move["pieceType"], move["toCol"], move["toRow"], fen, stockfish,
        fromRow=move["fromRow"], fromCol=move["fromCol"])

    return f'{move["fromCol"]}{move["fromRow"]}{move["toCol"]}{move["toRow"]}{"" if move["promotion"] == 0 else move["promotion"].lower()}'
    # return whateverTilTall(move["fraRad"]), whateverTilTall(move["fraKol"]), whateverTilTall(move["tilRad"]), whateverTilTall(move["tilKol"]), None if not move["promotion"] else promotionMap[q][move["promotion"].lower()]
