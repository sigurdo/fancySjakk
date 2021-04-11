
import os
import generalFunctions
import drawingTools

class PieceRenderer:
    pieceBasePath = "ressurser/brikker/"

    sizePrefix = "storrelse_"

    pieceToFilePathMap = {
        " ": "tom.txt",
        "r": "spiller_sort/tarn.txt",
        "n": "spiller_sort/hest.txt",
        "b": "spiller_sort/surpomp.txt",
        "q": "spiller_sort/dronning.txt",
        "k": "spiller_sort/konge.txt",
        "p": "spiller_sort/bonde.txt",
        "R": "spiller_hvit/tarn.txt",
        "N": "spiller_hvit/hest.txt",
        "B": "spiller_hvit/surpomp.txt",
        "Q": "spiller_hvit/dronning.txt",
        "K": "spiller_hvit/konge.txt",
        "P": "spiller_hvit/bonde.txt"
    }

    def __init__(self, cellWidth, cellHeight):
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
    
    def testMe(self):
        # print(drawingTools.addDrawingToBottom(drawingTools.stripDrawing(self.renderPieceRaw("r")), self.renderBottomWhite(), vOffset=1, hOffset=4, hSafezone=2))
        print(self.renderPiece("r", "black"))
    
    # Loops the piece base path and returns recognized sizes in a set of (width, height) tuples
    def findPieceSizes(self, piece):
        pieceSizes = set()
        for root, dirs, files in os.walk(self.pieceBasePath):
            for dirName in dirs:
                if dirName[:10] == self.sizePrefix:
                    # print(os.path.join(root, dirName, self.pieceToFilePathMap[piece]))
                    if os.path.exists(os.path.join(root, dirName, self.pieceToFilePathMap[piece])):
                        pieceSizes.add(tuple([int(num) for num in dirName[10:].split("x")]))
                    # width, height = int(width), int(height)
                    
                    # print("w, h", type(width))
                # print("dirr:", dirName[:10])
        return pieceSizes
    
    # Returns the largest available size that fits in the cell size in both width and height as a tuple (width, height)
    def findBestPieceSize(self, piece):
        availablePieceSizes = self.findPieceSizes(piece)
        maxFittingSize = (0, 0)
        for width, height in availablePieceSizes:
            if width <= self.cellWidth and height <= self.cellHeight and width >= maxFittingSize[0] and height >= maxFittingSize[1]:
                maxFittingSize = (width, height)
        return maxFittingSize
    
    def renderBottomWhite(self):
        res = ""
        for i in range(self.cellHeight):
            if i != 0:
                res += "\n"
            for j in range(self.cellWidth):
                res += "X"
        return res
    
    def renderBottomBlack(self):
        res = ""
        for i in range(self.cellHeight):
            if i != 0:
                res += "\n"
            for j in range(self.cellWidth):
                res += " "
        return res
    
    # Same as renderPiece, but without bottom color and size adjustments
    def renderPieceRaw(self, piece):
        bestWidth, bestHeight = self.findBestPieceSize(piece)
        return generalFunctions.readTxtFile(os.path.join(self.pieceBasePath, f"{self.sizePrefix}{bestWidth}x{bestHeight}", self.pieceToFilePathMap[piece]))
    
    # Returns a rendered instance of the given piece on the given bottom color
    # Parameters:
    #   piece (str) - one of: r, n, b, q, k, p, R, N, B, Q, K, P
    #   bottomColor (str) - one of: white, black
    def renderPiece(self, piece, bottomColor):
        raw = self.renderPieceRaw(piece)
        stripped = drawingTools.stripDrawing(raw)

        if stripped == "":
            width, height = 0, 0
        else:
            temp = stripped.split("\n")
            width, height = len(temp[0]), len(temp)
        
        hOffset = (self.cellWidth - width) // 2
        vOffset = self.cellHeight - height

        cell = drawingTools.addDrawingToBottom(stripped, self.renderBottomWhite() if bottomColor == "white" else self.renderBottomBlack(), hSafezone=1, hOffset=hOffset, vOffset=vOffset)
        return cell
