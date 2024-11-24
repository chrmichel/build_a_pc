from collections import deque, Counter

def push_d() -> list[str]:
    return [
        "@SP", "AM=M+1", "A=A-1", "M=D"
    ]

def push_0() -> list[str]:
    return [
        "@SP", "AM=M+1", "A=A-1", "M=0"
    ]

def pop_d() -> list[str]:
    return [
        "@SP", "AM=M-1", "D=M"
    ]
def pop_a() -> list[str]:
    return [
        "@SP", "AM=M-1", "A=M"
    ]

segments: dict[str, str] = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS", 
    "that": "THAT"
}

def bootstrap() -> list[str]:
    return ["# bootstrap", "@256", "D=A", "@SP", "M=D",
            "@300", "D=A", "@LCL", "M=D",
            "@400", "D=A", "@ARG", "M=D",
            "@3000", "D=A", "@THIS", "M=D",
            "@3010", "D=A", "@THAT", "M=D"
            ]

def push_static(file: str, idx: str) -> list[str]:
    return ["# push static " + idx, f"@{file}.{idx}", "D=M"] + push_d()

def push_latt(segment: str, index: str) -> list[str]:
    return [
        " ".join(["# push", segment, index]), 
        f"@{index}", "D=A", "@"+segment, "A=M", "A=D+A", "D=M"
    ] + push_d()

def push_temp(index: str) -> list[str]:
    return [
        "# push temp " + index, "@5", "D=A", "@"+index, "A=D+A", "D=M"
    ] + push_d()

def push_pointer(value: str) -> list[str]:
    addr: str = str(3 + int(value))
    return ["# push pointer " + value, "@" + addr, "D=M"] + push_d()

def push(segment: str, value: str) -> list[str]:
    
    match segment:
        case "constant":
            return ["# push constant " + value, f"@{value}", "D=A"] + push_d()
        case segment if segment in segments.keys():
            return push_latt(segments[segment], value)
        case "temp":
            return push_temp(value)
        case _:
            return []

def pop_static(file: str, idx: str) -> list[str]:
    return ["# pop static " + idx] + pop_d() + [ f"@{file}.{idx}", "M=D"]

def pop_latt(segment: str, index: str) -> list[str]:
    return [" ".join(["# pop", segment, index]),
            "@"+segment, "D=M", "@"+index, "D=D+A", "@R13", "M=D"] + pop_d() + ["@R13", "A=M", "M=D"]

def pop_temp(index: str) -> list[str]:
    return [
        "# pop temp " + index, "@5", "D=A", "@"+index, "D=D+A", "@R13", "M=D"
    ] + pop_d() + ["@R13", "A=M", "M=D"]

def pop_pointer(value: str) -> list[str]:
    addr: str = str(3 + int(value))
    return ["# pop pointer " + value] + pop_d() + [ "@" + addr, "M=D"]

def pop(segment: str, value: str) -> list[str]:
    match segment:
        case segment if segment in segments.keys():
            return pop_latt(segment, value)
        case "temp":
            return pop_temp(value)
        case _:
            return []

def parse_branch(command: str, label: str) -> list[str]:
    match command:
        case "label":
            return [f"({label})"]
        case "goto":
            return [f"@{label}", "0;JMP"]
        case "if-goto":
            return ["# if-goto"] +  pop_d() + [f"@{label}", "D;JNE"]
        case _:
            return []
        

def parse_compare(command: str, label: str) -> list[str]:
    cmp: str = command.upper()
    return [f"# {command}"] + pop_d() + ["A=A-1", "D=M-D", "M=-1", "@"+label, "D;J"+cmp, "@SP", "A=M-1", "M=0", f"({label})"]

def parse_math(command: str) -> list[str]:
    match command:
        case "add":
            return ["# add"] + pop_d() + ["A=A-1", "M=D+M"]
        case "sub":
            return ["# sub"] + pop_d() + ["A=A-1", "M=M-D"]
        case "and":
            return ["# and"] + pop_d() + ["A=A-1", "M=D&M"]
        case "or":
            return ["#  or"] + pop_d() + ["A=A-1", "M=D|M"]
        case "not":
            return ["# not", "@SP", "A=M-1", "M=~M"]
        case "neg":
            return ["# neg", "@SP", "A=M-1", "M=-M"]
        case _:
            return []
        
def parse_call(fname: str, nArgs: str, returnlabel: str) -> list[str]:
    answer: list[str] = [
        " ".join(["# call", fname, nArgs])
    ]
    # save caller frame
    answer += ["@"+returnlabel, "D=A"] + push_d()
    answer += ["@LCL", "D=M"] + push_d()
    answer += ["@ARG", "D=M"] + push_d()
    answer += ["@THIS", "D=M"] + push_d()
    answer += ["@THAT", "D=M"] + push_d()
    # set ARG to SP - 5 - nArgs
    answer += ["@5", "D=A", "@"+nArgs, "D=D+A", "@SP", "D=M-D", "@ARG", "M=D"]
    # set LCL to SP
    answer += ["@SP", "D=M", "@LCL", "M=D"]
    # goto function
    answer += ["@"+fname, "0;JMP"]
    # set return label
    answer += [f"({returnlabel})"]
    return answer

def parse_function(fname: str, nVars: int) -> list[str]:
    answer: list[str] = [f"({fname})"]
    for _ in range(nVars):
        answer += push_0()
    return answer

def parse_return() -> list[str]:
    answer: list[str] = ["# return"]
    # save endFrame in R13
    answer += ["@LCL", "D=M", "@R13", "M=D"]
    # save retAddr in R14
    answer += ["@5", "A=D-A", "D=M", "@R14", "M=D"]
    # move return value to ARG
    answer += pop_d() + ["@ARG", "A=M", "M=D"]
    # SP = ARG+1
    answer += ["@ARG", "D=M", "@SP", "M=D+1"]
    # restore THAT, THIS, ARG, LCL
    for seg in ["THAT", "THIS", "ARG", "LCL"]:
        answer += ["@R13", "AM=M-1", "D=M", f"@{seg}", "M=D"]
    # return to retAddr
    answer += ["@R14", "A=M;JMP"]
    return answer

class Translator:
    def __init__(self, file: str) -> None:
        self.filename: str = file
        self.cmp_count: Counter[str] = Counter()
        self.ret_count: Counter[str] = Counter()
        self.callstack: deque[str] = deque()
    
    @property
    def curr_func(self) -> str:
        return f"{self.filename}.{self.callstack[-1]}"

    def set_func_prefix(self, name: str) -> str:
        """ add class name in front of function name, if not already present
        """
        if not name.startswith(self.filename + "."):
            name = "".join([self.filename, ".", name])
        return name
    
    def fix_call_prefix(self, name: str) -> str:
        """ if `name` does not start with a class name, append own class name
        """
        words = name.split(".", 1)
        if len(words) == 1:
            return self.filename + "." + name
        return name
    
    def create_return_label(self) -> str:
        """ create return label of the shape `Class.function$ret.i`
        """
        self.ret_count[self.curr_func] += 1
        return f"{self.curr_func}$ret.{self.ret_count[self.curr_func]}"
    
    def create_compare_label(self) -> str:
        """ create compare label of the shape `Class.function$cmp.i`
        """
        self.cmp_count[self.curr_func] += 1
        return f"{self.curr_func}$cmp.{self.cmp_count[self.curr_func]}"

    def parse_pushpop(self, cmd: str, segment: str, value: str) -> list[str]:
        match cmd:
            case "push":
                if segment == "static":
                    return push_static(self.filename, value)
                elif segment == "pointer" and value in "01":
                    return push_pointer(value)
                return push(segment, value)
            
            case "pop":
                if segment == "static":
                    return pop_static(self.filename, value)
                elif segment == "pointer" and value in "01":
                    return pop_pointer(value)
                return pop(segment, value)
            case _:
                return []
            
    def translate(self, words: list[str]) -> list[str]:
        match words:
            case []:
                return []
            case [str(math)] if math in ["add", "sub", "neg", "gt", "and", "or", "not"]:
                return parse_math(math)
            case [str(comp)] if comp in ["eq", "lt", "gt"]:
                label: str = self.create_compare_label()
                return parse_compare(comp, label)
            case ["return"]:
                self.callstack.pop()
                return parse_return()
            case[str(branch), str(label)] if branch in ["label", "goto", "if-goto"]:
                return parse_branch(branch, label)
            case [str(cmd), str(segment), str(value)] if cmd in ["push", "pop"] and value.isnumeric():
                return self.parse_pushpop(cmd, segment, value)
            case [str(cmd), str(funcname), str(value)] if cmd == "function" and value.isnumeric():
                funcname = self.set_func_prefix(funcname)
                return parse_function(funcname, int(value))
            case [str(cmd), str(funcname), str(value)] if cmd == "call" and value.isnumeric():
                funcname = self.fix_call_prefix(funcname)
                retlabel: str = self.create_return_label()
                self.callstack.append(funcname)
                return parse_call(funcname, value, retlabel)
            case  _:
                return []