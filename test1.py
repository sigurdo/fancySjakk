import urwid
import argparse
import pyfiglet

parser = argparse.ArgumentParser(description="Fancy sjakk")
# parser.add_argument("--dahlspath", metavar="dahlspath", type=str, default="dahls.txt")
args = parser.parse_args()

def readTxt(filepath):
    with open(filepath, "r") as file:
        return file.read()

def unhandled_input(key):
    if key == "t":
        drawBoard(boardMatrix)
        return
    raise urwid.ExitMainLoop()

def drawBoard(boardMatrix):
    tomTxtW = readTxt("ressurser/brikker/bunn_hvit/tom.txt")
    tomTxtB = readTxt("ressurser/brikker/bunn_sort/tom.txt")

    rows = []
    for i in range(8):
        cols = []
        number = pyfiglet.Figlet().renderText(chr(0x38 - i))
        number = urwid.Text(number, align="center")
        number = urwid.Padding(number, width=16)
        # number = urwid.BoxAdapter(urwid.Filler(number, min_height=7, valign="bottom"), 7)
        cols.append(number)
        for j in range(8):
            txt = readTxt("ressurser/brikker/bunn_hvit/spiller_sort/tarn.txt")
            col = urwid.Text(txt)
            col = urwid.Padding(col)
            cols.append(col)
        row = urwid.Columns(cols)
        rows.append(row)
    cols = []
    cols.append(urwid.Padding(urwid.BoxAdapter(urwid.SolidFill(), height=7), width=16))
    for i in range(1, 9):
        letter = pyfiglet.Figlet().renderText(chr(0x40 + i))
        letter = urwid.Text(letter, align="center")
        letter = urwid.Padding(letter, width=16)
        cols.append(letter)
    row = urwid.Columns(cols)
    rows.append(row)
    board.contents = [(row, board.options()) for row in rows]

boardMatrix = [['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
         ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
         ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']]

tomTxtW = readTxt("ressurser/brikker/bunn_hvit/tom.txt")
tomTxtB = readTxt("ressurser/brikker/bunn_sort/tom.txt")

rows = []
for i in range(8):
    cols = []
    number = pyfiglet.Figlet().renderText(chr(0x38 - i))
    number = urwid.Text(number, align="center")
    number = urwid.Padding(number, width=16)
    # number = urwid.BoxAdapter(urwid.Filler(number, min_height=7, valign="bottom"), 7)
    cols.append(number)
    for j in range(8):
        txt = tomTxtW if (i + j) % 2 == 0 else tomTxtB
        col = urwid.Text(txt)
        col = urwid.Padding(col)
        cols.append(col)
    row = urwid.Columns(cols)
    rows.append(row)
cols = []
cols.append(urwid.Padding(urwid.BoxAdapter(urwid.SolidFill(), height=7), width=16))
for i in range(1, 9):
    letter = pyfiglet.Figlet().renderText(chr(0x40 + i))
    letter = urwid.Text(letter, align="center")
    letter = urwid.Padding(letter, width=16)
    cols.append(letter)
row = urwid.Columns(cols)
rows.append(row)
board = urwid.Pile(rows)
topWidget = urwid.Padding(board, width=16 * 8 + 16)
topWidget = urwid.Filler(topWidget)

# rows = [urwid.Columns([urwid.Padding(urwid.Text(tomTxtW if (i + j) % 2 == 0 else tomTxtB), width=16) for j in range(8)]) for i in range(8)]
# for i in range(len(rows)):
#     txt = pyfiglet.Figlet().renderText(chr(0x41 + i))
#     rows[i].contents.insert(0, (urwid.Padding(urwid.Text(txt), width=16), ('pack', None, None)))
# topWidget = urwid.Filler(urwid.Padding(urwid.Pile(rows), width=16 * 8 + 16))

loop = urwid.MainLoop(topWidget, unhandled_input=unhandled_input)
loop.run()
