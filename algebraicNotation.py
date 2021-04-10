import generalFunctions
import fenReader
import numpy as np

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
    toRowNr = rows.index(toRow)
    toColNr = cols.index(toCol)

    possibleFroms = []
    for row in rows:
        if fromRow and fromRow != row: continue
        for col in cols:
            if fromCol and fromCol != col: continue
            rowNr = rows.index(row)
            colNr = cols.index(col)
            if (boardMatrix[rowNr][colNr] == piece):
                # print(f"{col}{row}{toCol}{toRow}")
                try:
                    indicesToUci(rowNr, colNr, toRowNr, toColNr, fen, stockfish)
                    possibleFroms.append((col, row))
                except Exception:
                    pass

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

# Arguments:
# - rowNr     - index in board matrix of row to move from, one of 0, 1, 2, 3, 4, 5, 6, 7
# - colNr     - index in board matrix of col to move from, one of 0, 1, 2, 3, 4, 5, 6, 7
# - toRowNr   - index in board matrix of row to move to,   one of 0, 1, 2, 3, 4, 5, 6, 7
# - toColNr   - index in board matrix of col to move to,   one of 0, 1, 2, 3, 4, 5, 6, 7
# - fen       - fen position of board before performing move
# - stockfish - stockfish.Stockfish instance
# - preferredPromotion="q" - if promotion is available promote to this piece type, one of "q", "r", "b", "n"
#
# Returns:
# - uci - uci notation for the move f ex "d3d6"
#
# Exceptions:
# - Raises Exception if attempted move is illegal, so no need to check additionally
def indicesToUci(rowNr, colNr, toRowNr, toColNr, fen, stockfish, preferrdPromotion="q"):
    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
    move = f'{cols[colNr]}{rows[rowNr]}{cols[toColNr]}{rows[toRowNr]}'
    stockfish.set_fen_position(fen)
    if not stockfish.is_move_correct(move):
        move += preferrdPromotion
        if not stockfish.is_move_correct(move):
            raise Exception(f'Move is illegal: {move}')
    return move

# Arguments:
# - uci - uci notation for the move f ex "d3d6"
# - fen - fen position of board before performing move
# - stockfish - stockfish.Stockfish instance
#
# Returns:
# - algebraic - algebraic notaion for the move, f ex "Rxd6"
#
# NOTE: One big downside with this function is that it does not add + and # at the end for checks and checkmates, because I could not find
# a single way to determine that by using stockfish, so I will more or less have to code my own engine, and that is a lot of work
def uciToAlg(uci, fen, stockfish):
    rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]

    stockfish.set_fen_position(fen)
    if not stockfish.is_move_correct(uci):
        raise Exception(f'Move is not valid: {uci}')

    boardMatrix = fenReader.getBoardMatrix(fen)
    move = {
        "player": 0,
        "pieceType": 0,
        "fromCol": 0,
        "fremRow": 0,
        "capture": 0,
        "toCol": 0,
        "toRow": 0,
        "promotion": 0,
        "check": 0,
    }
    move["player"] = fenReader.getPlayerInMove(fen)
    move["fromCol"] = uci[0]
    move["fromRow"] = uci[1]
    move["toCol"] = uci[2]
    move["toRow"] = uci[3]
    fromColNr = cols.index(move["fromCol"])
    fromRowNr = rows.index(move["fromRow"])
    toColNr = cols.index(move["toCol"])
    toRowNr = rows.index(move["toRow"])
    move["pieceType"] = boardMatrix[fromRowNr][fromColNr].upper()
    move["capture"] = "" if boardMatrix[toRowNr][toColNr] == " " else "x"
    if len(uci) > 4:
        move["promotion"] = uci[4].upper()

    try:
        findPieceTo(move["pieceType"], move["toCol"], move["toRow"], fen, stockfish)
        specifyFrom = False
    except:
        specifyFrom = True

    if move["pieceType"] == "K" and move["fromCol"] == "e" and move["toCol"] == "g": return "0-0"
    elif move["pieceType"] == "K" and move["fromCol"] == "e" and move["toCol"] == "c": return "0-0-0"

    algebraic = ""
    if move["pieceType"] != "P":
        algebraic += move["pieceType"]
    if specifyFrom:
        algebraic += move["fromCol"]
        algebraic += move["fromRow"]
    algebraic += move["capture"]
    algebraic += move["toCol"]
    algebraic += move["toRow"]
    if move["promotion"]:    
        algebraic += "="
        algebraic += move["promotion"]
    if move["check"]:
        algebraic += move["check"]

    return algebraic
