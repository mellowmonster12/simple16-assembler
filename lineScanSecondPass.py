import classes
import lineConvert
def smartLineConvert(line:str,labels:dict,clabels:dict):
    if line[0] == ";" or line[:5].upper() == "LABEL" or line[:6].upper() == "CLABEL": #doesn't even bother trying to decode the line if it's not needed. it simply compiles NOP in case it gets in there somehow.
        return classes.line("07",True,"0000","0000",True,True,"0000") #this equates to "NOP"
    else: 
        return lineConvert.LineConvert(line,labels,clabels)
def scan(code:str, labels:dict,clabels:dict):
    split = code.split("\n") #this is how code is split

    return [smartLineConvert(line,labels,clabels) for line in split] #yeah, i made it a separate function to put it in a single list comprehension.
