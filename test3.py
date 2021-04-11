import urwid
import urwid.curses_display

log = []

def inputCallback(widget, text):
    log.append(text+", "+inputWidget.get_edit_text())
    if text.endswith("\n"):
        raise urwid.ExitMainLoop()

inputWidget = urwid.Edit(caption="yo: ", multiline=True)

urwid.connect_signal(inputWidget, "change", inputCallback)

topWidget = urwid.Filler(inputWidget)

loop = urwid.MainLoop(topWidget, screen=urwid.curses_display.Screen())
loop.run()

print(log)
