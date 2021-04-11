import urwid
import urwid.curses_display
import argparse
from importSettings import settings
import ChessGame

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

def drawScreen():
    loop.draw_screen()

def exitGame():
    raise urwid.ExitMainLoop()

chessGame = ChessGame.ChessGame(drawScreen, exitGame)
loop = urwid.MainLoop(chessGame.topWidget, unhandled_input=chessGame.unhandled_input, screen=urwid.curses_display.Screen())
loop.run()
# chessGame.start()
# chessGame.testing()
