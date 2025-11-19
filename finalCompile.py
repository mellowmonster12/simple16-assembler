import classes
import lineScanFirstPass
import lineScanSecondPass
import numpy

if __name__ != "__main__":
    exit() #this cannot be used as a library

def assembleLine(line:classes.line): #this converts the line class into a useable hexadecimal number that can be imported into logisim
    constantByte:numpy.uint8 = numpy.uint8(0)
    if line.param1Const:
        constantByte = numpy.uint8(constantByte + 1)
    if line.param2Const:
        constantByte = numpy.uint8(constantByte + 2)
    if line.isBLU:
        constantByte = numpy.uint8(constantByte + 4)
    return line.destination + line.param2 + line.param1 + f"{constantByte:02X}" + line.operation

print("SimpleASM assembler - assembly for Simple16")
fileName = input("please input the path to the assembly file (include any file extensions) \n")
outFile = input("what shall be the name of the file? (include any file extensions) \n")
with open(fileName) as f:
    assembly = f.read()
print("doing first pass...")
firstPassResults = lineScanFirstPass.scan(assembly)
print("first pass done.")
print("doing second pass...")
secondPassResults = lineScanSecondPass.scan(assembly,firstPassResults["labels"],firstPassResults["clabels"])
print("second pass completed")
print("now compiling...")
assembled = [assembleLine(line) for line in secondPassResults]
i = 0
final = []
for line in assembled:
    if not firstPassResults["lineNumbers"][i] == firstPassResults["lineNumbers"][i-1]: #the way this was designed, i made it so first line with a line number is the only one that makes it. this enables lines like 'label jump' easier to implement
        final.append(line)
    i += 1
output = ""
for line in final: #finally, the list gets turned into a neat text that is able to be imported to logisim
    output = output + line + "\n"

print("compiled succesfully, writing to file")

with open(outFile,"wt") as f:
    f.write(output)

print("done")
input("")

exit()
