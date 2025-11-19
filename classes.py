class operation():
    name:str = ""
    isBLU:bool = False
    OperationCount:int = 2
    number:int = 0
    def __init__(self, name:str, isBLU:bool, OpCount:int,number:int) -> None:
        self.name = name
        self.isBLU = isBLU
        self.OperationCount = OpCount
        self.number = number

class line():
    operation:str = "00"
    isBLU:bool = False
    param1:str = "0000"
    param2:str = "0000"
    param1Const:bool = False
    param2Const:bool = False
    destination:str = "0000"
    def __init__(self,op:str,isBLU:bool, param1:str, param2:str,param1Const:bool,Param2Const:bool,destination:str) -> None:
        self.operation = op
        self.isBLU = isBLU
        self.param1 = param1
        self.param2 = param2
        self.param1Const = param1Const
        self.param2Const = Param2Const
        self.destination = destination

class CompilationError(SyntaxError):
    pass

class OpNotFoundError(CompilationError):
    pass

class InvalidPrefix(CompilationError):
    pass

class OpNumError(CompilationError):
    pass