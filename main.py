import urwid
import argparse
import pyfiglet
import PieceRenderer

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

# Using FEN notaton for each piece 
boardMatrix = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

def readTxtFile(filepath):
    with open(filepath, "r") as file:
        return file.read()

class BoardDrawer:
    pieceTextWidgets = []
    letterTextWidgets = []
    numberTextWidgets = []

    def __init__(self):
        self.pieceRenderer = PieceRenderer.PieceRenderer(16, 7)

        # Create piece widgets
        for i in range(8):
            self.pieceTextWidgets.append([])
            for j in range(8):
                field = urwid.Text("")

                # Sette bakgrunnsfarger:
                tomTxtW = self.pieceRenderer.renderBottomWhite()
                tomTxtB = self.pieceRenderer.renderBottomBlack()
                field.set_text(tomTxtW if (i + j) % 2 == 0 else tomTxtB)

                self.pieceTextWidgets[i].append(field)
        
        # Create letter widgets
        for i in range(1, 9):
            text = pyfiglet.Figlet().renderText(chr(0x40 + i))
            textWid = urwid.Text(text, align="center")
            self.letterTextWidgets.append(textWid)
        
        # Create number widgets
        for i in range(8, 0, -1):
            text = pyfiglet.Figlet().renderText(str(i))
            textWid = urwid.Text(text, align="center")
            self.numberTextWidgets.append(textWid)

        # Place widgets in piles and columns
        widgetRows = []
        for i in range(len(self.pieceTextWidgets)):
            row = self.pieceTextWidgets[i].copy()
            row.insert(0, self.numberTextWidgets[i])
            row.append(self.numberTextWidgets[i])
            widgetRows.append(urwid.Columns(row))
        numberRow = urwid.Columns(self.letterTextWidgets)
        numberRow = urwid.Padding(numberRow)
        numberRow.left = 16
        numberRow.right = 16
        widgetRows.append(numberRow)
        widgetRows.insert(0, numberRow)
        
        self.topWidget = urwid.Pile(widgetRows)
        self.topWidget = urwid.Padding(self.topWidget, width=16 * 10)
        self.topWidget = urwid.Filler(self.topWidget)
        
        self.loop = urwid.MainLoop(self.topWidget, unhandled_input=self.unhandled_input)
        self.loop.run()
    
    def unhandled_input(self, key):
        if key == "t":
            self.setPieces(boardMatrix)
            return
        raise urwid.ExitMainLoop()

    def setPieces(self, boardMatrix):
        for i in range(8):
            for j in range(8):
                text = self.pieceRenderer.renderPiece(boardMatrix[i][j], "white" if (i + j) % 2 == 0 else "black")
                self.pieceTextWidgets[i][j].set_text(text)

boardDrawer = BoardDrawer()
