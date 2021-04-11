import urwid
import urwid.curses_display
import argparse
import pyfiglet
import BoardDrawer
import stockfish
from importSettings import settings
import time
import generalFunctions
import algebraicNotation

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class ChessGame:
    log = []

    def __init__(self):
        self.stockfish = stockfish.Stockfish(settings.stockfishPath)

        self.boardDrawer = BoardDrawer.BoardDrawer()
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

        self.palette = [
            ("whiteCell", "black", "light gray"),
            ("blackCell", "", "black"),
        ]

        self.loop = urwid.MainLoop(self.topWidget, unhandled_input=self.unhandled_input, screen=urwid.curses_display.Screen(), palette=self.palette)

    def start(self):
        self.loop.run()

    def testing(self):
        self.stockfish.set_position(["e2e4", "e7e6"])
        print(self.stockfish.get_board_visual())
        print(self.stockfish.get_fen_position())
        self.boardDrawer.setPieces(self.stockfish.get_fen_position())
        print(algebraicNotation.algToUci("e4", startFen, self.stockfish))
        fen = "rnbqkbnr/ppppppPp/8/p7/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.stockfish.set_fen_position(fen)
        print(self.stockfish.get_board_visual())
        print(algebraicNotation.algToUci("xh8=Q", fen, self.stockfish))

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
    
    # Uses self.log to set correct contents of self.logWidget
    def updateLogWidget(self):
        algLog = []
        for i, move in enumerate(self.log):
            self.stockfish.set_position(self.log[:i])
            fen = self.stockfish.get_fen_position()
            algLog.append(algebraicNotation.uciToAlg(move, fen, self.stockfish))
        self.logWidget.set_text(generalFunctions.joinListToString(algLog, sep="\n"))

    
    def userInputEnter(self):
        inputText = self.inputWidget.get_edit_text()
        if inputText == "q":
            raise urwid.ExitMainLoop()
        
        try:
            move = algebraicNotation.algToUci(inputText, self.stockfish.get_fen_position(), self.stockfish)
        except:
            move = inputText

        if move != "" and self.stockfish.is_move_correct(move):
            self.log.append(move)
            self.updateLogWidget()
            self.stockfish.set_position(self.log)
            self.boardDrawer.setPieces(self.stockfish.get_fen_position())
            self.loop.draw_screen()
            time.sleep(0.2)
            # self.log.append(self.stockfish.get_best_move())
            self.updateLogWidget()
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
