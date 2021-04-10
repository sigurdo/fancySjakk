import urwid
import pyfiglet
import PieceRenderer
import generalFunctions
import fenReader

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

    def setPieces(self, fen):
        boardMatrix = fenReader.getBoardMatrix(fen)
        for i in range(8):
            for j in range(8):
                text = self.pieceRenderer.renderPiece(boardMatrix[i][j], "white" if (i + j) % 2 == 0 else "black")
                self.pieceTextWidgets[i][j].set_text(text)
