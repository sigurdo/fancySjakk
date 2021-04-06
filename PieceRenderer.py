
import os

class PieceRenderer:
    pieceBasePath = "ressurser/brikker/"

    sizePrefix = "storrelse_"

    pieceToFilePathMap = {
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
        availablePieceSizes = self.findPieceSizes("r")
        bestSize = self.findBestPieceSize("r")
        # self.pieceSize = 

        print(bestSize)
        print(self.stripDrawing(self.renderPieceRaw("r")))
        print(self.renderBottomBlack())
        print(self.renderBottomWhite())
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("r")), self.renderBottomWhite(), vOffset=1, hOffset=4, hSafezone=2))
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("R")), self.renderBottomWhite(), vOffset=1, hOffset=6, hSafezone=2))
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("N")), self.renderBottomWhite(), vOffset=2, hOffset=4, hSafezone=2))
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("q")), self.renderBottomWhite(), vOffset=1, hOffset=4, hSafezone=2))
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("k")), self.renderBottomWhite(), vOffset=1, hOffset=4, hSafezone=2))
        print(self.addDrawingToBottom(self.stripDrawing(self.renderPieceRaw("p")), self.renderBottomWhite(), vOffset=1, hOffset=-4, hSafezone=2))
        return
    
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
    
    def joinListToString(self, listToJoin, sep=""):
        res = ""
        for item in listToJoin:
            if res != "":
                res += sep
            res += item
        return res
    
    def getContentBorders(self, line):
        content = line.strip(" ")
        start = line.index(content[0])
        end = len(line) - 1 - line[::-1].index(content[len(content) - 1])
        return start, end
    
    def stripDrawing(self, drawing):
        # Deassemble drawing into list of lines
        lines = drawing.split("\n")

        # Strip empty lines from top and bottom
        toDelete = set()
        for i in range(len(lines)):
            line = lines[i]
            if line.strip(" ") != "":
                break
            toDelete.add(i)
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            if line.strip(" ") != "":
                break
            toDelete.add(i)
        # Note: This loop must be reversed, because if not, indexes will change as elements gets deleted
        for i in reversed(list(toDelete)):
            del lines[i]

        # Find maximum and minimum horizontal positions for actual characters
        minStart = None
        maxEnd = None
        for line in lines:
            start, end = self.getContentBorders(line)
            print(start, end)
            if minStart == None or start < minStart:
                minStart = start
            if maxEnd == None or end > maxEnd:
                maxEnd = end
        
        # Strip anything outside these borders
        for i, line in enumerate(lines):
            lines[i] = line[minStart:maxEnd + 1]

        # Reassemble drawing
        drawing = self.joinListToString(lines, sep="\n")
        
        return drawing
    
    def addDrawingToBottom(self, drawing, bottom, vOffset=0, hOffset=0, hSafezone=0):
        lines = bottom.split("\n")
        drawingLines = drawing.split("\n")

        for i in range(min(len(drawingLines), len(lines) - vOffset)):
            if vOffset + i < 0:
                continue
            line = lines[vOffset + i]
            drawingLine = drawingLines[i]
            start, end = self.getContentBorders(drawingLine)
            lines[vOffset + i] = line[:max(hOffset + start - hSafezone, 0)] + " " * hSafezone + drawingLine[max(start,-hOffset):end + 1] + " " * hSafezone + line[hOffset + end + 1 + hSafezone:]
            lines[vOffset + i] = lines[vOffset + i][:len(line)]

        return self.joinListToString(lines, sep="\n")
    
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
    
    def readTxtFile(self, filepath):
        with open(filepath, "r") as file:
            return file.read()
    
    # Same as renderPiece, but without bottom color and size adjustments
    def renderPieceRaw(self, piece):
        bestWidth, bestHeight = self.findBestPieceSize(piece)
        return self.readTxtFile(os.path.join(self.pieceBasePath, f"{self.sizePrefix}{bestWidth}x{bestHeight}", self.pieceToFilePathMap[piece]))
    
    # Returns a rendered instance of the given piece on the given bottom color
    # Parameters:
    #   piece (str) - one of: r, n, b, q, k, p, R, N, B, Q, K, P
    #   bottomColor (str) - one of: white, black
    def renderPiece(self, piece, bottomColor):
        raw = self.renderPieceRaw(piece)
        stripped = self.stripDrawing(raw)
        return self.read