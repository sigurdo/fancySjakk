def joinListToString(listToJoin, sep=""):
    res = ""
    for item in listToJoin:
        if res != "":
            res += sep
        res += item
    return res
