import urwid
import urwid.curses_display
import argparse
import pyfiglet
import PieceRenderer
import stockfish
from importSettings import settings
import time
import generalFunctions

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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
    def getBoardMatrixFromFen(self, fen):
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

    def setPieces(self, fen):
        boardMatrix = self.getBoardMatrixFromFen(fen)
        for i in range(8):
            for j in range(8):
                text = self.pieceRenderer.renderPiece(boardMatrix[i][j], "white" if (i + j) % 2 == 0 else "black")
                self.pieceTextWidgets[i][j].set_text(text)

class ChessGame:
    log = []

    def __init__(self):
        self.stockfish = stockfish.Stockfish(settings.stockfishPath)

        self.boardDrawer = BoardDrawer()
        self.boardDrawer.setPieces(self.stockfish.get_fen_position())

        self.inputWidget = urwid.Edit(caption=">", edit_text="")
        inputContainer = self.inputWidget
        inputContainer = urwid.LineBox(inputContainer)
        inputContainer = urwid.Filler(inputContainer, valign="top")
        # inputContainer = urwid.Padding(inputContainer, align="center", width=30)

        urwid.connect_signal(self.inputWidget, "change", self.userInputKeystroke)

        self.logWidget = urwid.Text("")
        logContainer = self.logWidget
        logContainer = urwid.LineBox(logContainer)
        logContainer = urwid.Filler(logContainer, valign="bottom")
        # logContainer = urwid.

        logInputPile = urwid.Pile([logContainer, inputContainer])
        logInputPile = urwid.Padding(logInputPile, align="center", width=30)

        columns = urwid.Columns([(10 * 16, self.boardDrawer.topWidget), logInputPile])
        self.topWidget = urwid.Filler(columns, height=("relative", 100))

        self.loop = urwid.MainLoop(self.topWidget, unhandled_input=self.unhandled_input, screen=urwid.curses_display.Screen())

    def start(self):
        self.loop.run()

    def testing(self):
        self.stockfish.set_position(["e2e4", "e7e6"])
        print(self.stockfish.get_board_visual())
        print(self.stockfish.get_fen_position())
        self.boardDrawer.setPieces(self.stockfish.get_fen_position())

    def unhandled_input(self, key):
        if key == "q":
            raise urwid.ExitMainLoop()
        if key == "s":
            self.boardDrawer.setPieces(startFen)
            return
        if key == "t":
            self.stockfish.set_position(["e2e4", "e7e6"])
            self.boardDrawer.setPieces(self.stockfish.get_fen_position())
            return
        if key == "enter":
            self.userInputEnter()
            return
        # for i in range(100):
        #     print("unhandled input:", key)
    
    def userInputEnter(self):
        inputText = self.inputWidget.get_edit_text()
        if inputText == "q":
            raise urwid.ExitMainLoop()
        if self.stockfish.is_move_correct(inputText):
            self.log.append(inputText)
            self.logWidget.set_text(generalFunctions.joinListToString(self.log, sep="\n"))
            self.stockfish.set_position(self.log)
            self.boardDrawer.setPieces(self.stockfish.get_fen_position())
            self.loop.draw_screen()
            time.sleep(0.2)
            self.log.append(self.stockfish.get_best_move())
            self.logWidget.set_text(generalFunctions.joinListToString(self.log, sep="\n"))
            self.stockfish.set_position(self.log)
            self.boardDrawer.setPieces(self.stockfish.get_fen_position())
            self.inputWidget.set_edit_text("")

    def userInputKeystroke(self, widget, text):
        # self.stockfish.set_position([text])
        # self.boardDrawer.setPieces(self.stockfish.get_fen_position())
        pass

chessGame = ChessGame()
chessGame.start()
# chessGame.testing()
