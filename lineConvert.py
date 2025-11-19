import numpy as np #numpy is used to convert unusable float strings into usable hexadecimal. and to make sure that the values specified are 16-bit.
import classes
import rawOps
validDigits = [str(x) for x in range(1,9)]
ALUopNames = [item[0] for item in rawOps.ALUOPRaw]
BLUopNames = [item[0] for item in rawOps.BLUOPRaw]

def floatToHex(value: float) -> str: #this was added quite early in development. long before i uploaded this to github
    return f"{np.float16(value).view(np.uint16):04X}"

def ParamConvert(param:str,clabels:dict={}): #this turns the many types of parameters that simpleASM provides into the two the console is familiar with.
    constant = True
    trimmed = param[1:].upper()
    if param[0] == "U":
        constant = True
        number = f"{np.uint16(trimmed):04X}"
    elif param[0] == "C":
        constant = True
        number = f"{np.int16(trimmed):04X}"
    elif param[0] == "F":
        constant = True
        number = floatToHex(float(trimmed))
    elif param[0] == "H":
        constant = True
        number = f"{np.uint16(int(trimmed, 16)):04X}"
    elif param[0] == "R":
        constant = False
        number = f"{np.uint16(trimmed):04X}"
    elif param[0] == "O":
        number = f"{np.uint16(rawOps.ALU32OPRAW.index(trimmed)):04X}"
    elif param[0] == "A":
        number = f"{np.uint16(ord(trimmed)):04X}"
    elif param[0] == "L":
        try:
            number = f"{np.uint16(clabels[param[1:]]):04X}"
        except indexError:
            print(f"error: most likely, the c-label, {param[1:]}, does not exist.")
            input("press any key to exit...")
            exit()
    else:
        print(f"syntax error: {param[0]} is not a valid prefix.")
        input("press any key to exit...")
        exit()
    return [number,constant]

def LineConvert(line:str,jmpLocations:dict,clabels:dict) -> classes.line: #converts lines to the line class, which is then proccessed into more usuable numbers, which is then put into a usable format.
    split = line.split(" ") #this line is why 'MOV R1 R0 comment' is valid.
    if split[0].upper() in ALUopNames:
        IsBLU = False
        index = ALUopNames.index(split[0].upper())
    elif split[0].upper() in BLUopNames:
        IsBLU = True
        index = BLUopNames.index(split[0].upper())
    else:
        print(f"syntax error: {split[0]} is not an ALU or BLU operation.")
        input("press any key to contiunue...")
        exit()
    if not IsBLU:
        paramNum = rawOps.ALUOPRaw[index][1]
    else:
        paramNum = rawOps.BLUOPRaw[index][1]
    P1:list = ["0000",True]
    P2:list = P1
    if paramNum == 0: #i think i could've made this a bit better
        P1 = ["0000",True]
        P2 = ["0000",True]
    elif paramNum == 1:
        P1 = ParamConvert(split[1],clabels)
        P2 = ["0000",True]
    elif paramNum == 2:
        P1 = ParamConvert(split[1],clabels)
        P2 = ParamConvert(split[2],clabels)
    else:
        print(f"error: the instruction {split[0]} does not have a valid amount of operands. {paramNum} operands. (excluding destination operand, if it's there) this an issue on the assembler side.")
        input("press any key to exit...")
        exit()
    destIndex = paramNum + 1
    if not IsBLU:
        try:
            if split[destIndex][0] != "R" and not split[destIndex][0] in validDigits:
                if clabels[split[destIndex]][0].upper() == "R":
                    dest = f"{np.uint8(clabels[split[destIndex]][1:]):04X}"
                else:
                    dest = f"{np.uint8(clabels[split[destIndex]]):04X}"
            else:
                if split[destIndex][0].upper() == "R":
                    dest = f"{np.uint8(split[destIndex][1:]):04X}"
                else:
                    dest = f"{np.uint8(split[destIndex]):04X}"
        except IndexError:
            print("error: attempted to access a non-existent character in destination part") #i could probably word this a bit better
            print(f"line at fault: {line}")
            input("press any key to exit...")
            exit()
    else:
        if rawOps.BLUOPRaw[index][2]:
            dest = f"{np.uint16(jmpLocations[split[destIndex]]):04X}"
        else:
            dest ="0000"

    return classes.line(f"{index:02X}",IsBLU,P1[0],P2[0],P1[1],P2[1],dest)
