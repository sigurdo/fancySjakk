import urwid
import urwid.curses_display
import argparse
import pyfiglet
from importSettings import settings
import time
import generalFunctions
import drawingTools
import ChessGame

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

class FigletButton(urwid.WidgetWrap):
    def __init__(self, label, onClick):
        self.label = label
        self.figletText = pyfiglet.Figlet(font="smslant").renderText(self.label)
        self.figletText = drawingTools.stripDrawing(self.figletText)
        # raise Exception(len(self.figletText.split("\n")))
        self.labelWidget = urwid.Text(self.figletText, align="center")
        self.labelWidget = urwid.AttrMap(self.labelWidget, "normal", "normal")
        self.widget = urwid.LineBox(self.labelWidget)
        self.hiddenButton = urwid.Button("this text should be invisible", onClick)
        super(FigletButton, self).__init__(self.widget)
    
    def selectable(self):
        return True
    
    def keypress(self, *args, **kwargs):
        return self.hiddenButton.keypress(*args, **kwargs)
    
    def mouse_event(self, *args, **kwargs):
        return self.hiddenButton.mouse_event(*args, **kwargs)

class Menu:
    def __init__(self):
        palette = [
            ("normal", "", ""),
            ("highlight", "black", "light gray"),
            ("highlightBorder", "dark red", "dark red"),
            ("title", "", ""),
        ]

        button1 = urwid.Button("Start spill", on_press=self.startGame)
        button1 = urwid.AttrMap(button1, "normal", "highlight")
        button2 = urwid.Button("Hjelp")
        button2 = urwid.AttrMap(button2, "normal", "highlight")
        # button3 = FigletButton("Hmmj", self.userInputEnter)
        # button3 = urwid.AttrMap(button3, "normal", "highlightBorder")
        button3 = urwid.Button("Avslutt", on_press=self.exitApp)
        button3 = urwid.AttrMap(button3, "normal", "highlight")
        pile = urwid.Pile([button1, button2, button3])
        self.topWidget = urwid.Filler(pile, valign=urwid.TOP)
        self.topWidget = urwid.Padding(self.topWidget, align=urwid.CENTER, width=40)

        title = pyfiglet.Figlet(font="ogre", width=1000).renderText("fancyChess")
        title = drawingTools.stripDrawing(title)
        width = len(title.split("\n")[0])
        # raise Exception(title)
        title = urwid.Text(title)
        title = urwid.AttrMap(title, "title")
        title = urwid.Padding(title, width=width, align=urwid.CENTER)
        title = urwid.Filler(title, valign=urwid.BOTTOM, bottom=1)

        self.topWidget = urwid.Pile([("weight", 1, title), ("weight", 2, self.topWidget)])
        # self.topWidget = urwid.Padding(self.topWidget, align=urwid.CENTER, width=80)

        self.loop = urwid.MainLoop(self.topWidget, palette=palette, unhandled_input=self.unhandled_input, screen=urwid.curses_display.Screen())

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
        if key == "enter":
            self.userInputEnter()
            return
        # for i in range(100):
        #     print("unhandled input:", key)

    def userInputEnter(self):
        pass

    def userInputKeystroke(self, widget, text):
        # self.stockfish.set_position([text])
        # self.boardDrawer.setPieces(self.stockfish.get_fen_position())
        pass

    def exitApp(self, widget):
        raise urwid.ExitMainLoop()

    def exitGame(self):
        # raise urwid.ExitMainLoop()
        self.loop.widget = self.topWidget
        self.loop.unhandled_input = self.unhandled_input
    
    def startGame(self, widget):
        game = ChessGame.ChessGame(self.loop.draw_screen, self.exitGame)
        self.loop.widget = game.topWidget
        self.loop.unhandled_input = game.unhandled_input


menu = Menu()
menu.start()
# chessGame.testing()
