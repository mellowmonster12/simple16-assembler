import classes
import lineConvert
def smartLineConvert(line:str,labels:dict,clabels:dict):
    if line[0] == ";" or line[:5].upper() == "LABEL" or line[:6].upper() == "CLABEL":
        return classes.line("07",True,"0000","0000",True,True,"0000") #this equates to "NOP start" assuming start is at line 0
    else:
        return lineConvert.LineConvert(line,labels,clabels)
def scan(code:str, labels:dict,clabels:dict):
    split = code.split("\n")
    return [smartLineConvert(line,labels,clabels) for line in split]