import urwid
import urwid.curses_display
import argparse
import pyfiglet
from importSettings import settings
import time
import generalFunctions

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

class FigletButton(urwid.WidgetWrap):
    def __init__(self, label, onClick):
        self.label = label
        self.figletText = pyfiglet.Figlet().renderText(self.label)
        self.figletText = self.stripDrawing(self.figletText) + "\n"
        # raise Exception(len(self.figletText.split("\n")))
        self.labelWidget = urwid.Text(self.figletText, align="center")
        self.labelWidget = urwid.AttrMap(self.labelWidget, "normal", "normal")
        self.widget = urwid.LineBox(self.labelWidget)
        self.hiddenButton = urwid.Button("this text should be invisible", onClick)
        super(FigletButton, self).__init__(self.widget)
    
    def getContentBorders(self, line):
        content = line.strip(" ")
        if len(content) == 0:
            return 0, 0
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
            if minStart == None or start < minStart:
                minStart = start
            if maxEnd == None or end > maxEnd:
                maxEnd = end
        
        # Strip anything outside these borders
        for i, line in enumerate(lines):
            lines[i] = line[minStart:maxEnd + 1]

        # Reassemble drawing
        drawing = generalFunctions.joinListToString(lines, sep="\n")
        
        return drawing
    
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
        ]

        button1 = urwid.Button("hei")
        button1 = urwid.AttrMap(button1, "normal", "highlight")
        button2 = urwid.Button("yo")
        button2 = urwid.AttrMap(button2, "normal", "highlight")
        button3 = FigletButton("Hmmj", self.userInputEnter)
        button3 = urwid.AttrMap(button3, "normal", "highlightBorder")
        pile = urwid.Pile([button1, button2, button3])
        self.topWidget = urwid.Filler(pile)
        self.topWidget = urwid.Padding(self.topWidget, width=40)

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

menu = Menu()
menu.start()
# chessGame.testing()
