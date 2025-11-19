import classes
import lineConvert

def scan(code:str): #this function gives each line a number. i had the idea of making it this way since before the very start of development
    lineIDs = []
    labels = {}
    clabels = {}
    split:list[str] = code.split("\n")
    PC = 0
    #LastLineLABEL = False
    for line in split:
        if not (line[0] == ";" or [x for x in line if x != " "] == [] or line[:5].upper() == "LABEL" or line == "" or line[:6].upper() == "CLABEL"): #you may have inferred it, but this checks for labels, c-labels, comments, and whitespace
            PC += 1
        elif line[:5].upper() == "LABEL":
            labels = labels | {line[6:]:PC+1}
        elif line[:6].upper() == "CLABEL":
            clabels = clabels | {line.split(" ")[1]:lineConvert.ParamConvert(line.split(" ")[2])[0]}
        lineIDs.append(PC)
    return {"labels":labels,"lineNumbers":lineIDs,"clabels":clabels}


