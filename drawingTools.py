import generalFunctions

def getContentBorders(line):
    content = line.strip(" ")
    if len(content) == 0:
        return 0, 0
    start = line.index(content[0])
    end = len(line) - 1 - line[::-1].index(content[len(content) - 1])
    return start, end

def stripDrawing(drawing):
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
        start, end = getContentBorders(line)
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

def addDrawingToBottom(drawing, bottom, vOffset=0, hOffset=0, hSafezone=0):
    lines = bottom.split("\n")
    drawingLines = drawing.split("\n")

    if drawingLines == [""]:
        drawingLines = []

    for i in range(min(len(drawingLines), len(lines) - vOffset)):
        if vOffset + i < 0:
            continue
        line = lines[vOffset + i]
        drawingLine = drawingLines[i]
        start, end = getContentBorders(drawingLine)
        lines[vOffset + i] = line[:max(hOffset + start - hSafezone, 0)] + " " * hSafezone + drawingLine[max(start,-hOffset):end + 1] + " " * hSafezone + line[hOffset + end + 1 + hSafezone:]
        lines[vOffset + i] = lines[vOffset + i][:len(line)]

    return generalFunctions.joinListToString(lines, sep="\n")
