from pathlib import Path
from src.instruction import Instruction
from src.assembler.symboltable import SymbolTable

d_dict: dict[str, str] = {
    "null": "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "ADM": "111",
}
j_dict: dict[str, str] = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}
c_dict: dict[str, str] = {
    "0": "0101000",
    "1": "0111111",
    "-1": "0101001",
    "D": "0001100",
    "~D": "0001101",
    "-D": "0001111",
    "D-1": "0001110",
    "D+1": "0011111",
    "A": "0110000",
    "~A": "0110001",
    "-A": "0110011",
    "A-1": "0110010",
    "A+1": "0110111",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "~M": "1110001",
    "-M": "1110011",
    "M-1": "1110010",
    "M+1": "1110111",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}


class Parser:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.st = SymbolTable()
        self.asm_lines: list[str] = []
        self.asm_filtered: list[str] = []
        self.instructions: list[Instruction] = []

    def read_asm(self, file: str) -> None:
        path = Path("files/asm") / (file + ".asm")
        with path.open() as f:
            self.asm_lines = f.readlines()

    def write_hack(self, file: str) -> None:
        path = Path("files/hack") / (file + ".hack")
        with path.open("w") as f:
            f.writelines("\n".join([str(i) for i in self.instructions]))

    def is_c_instruction(self, line: str) -> tuple[bool, str, str, str]:
        dest_split = line.split("=", 1)
        if len(dest_split) > 1:
            dest: str = dest_split[0].strip()
            compjump: str = dest_split[1].strip()
        else:
            dest: str = "null"
            compjump: str = dest_split[0].strip()
        comp_split = compjump.split(";", 1)
        if len(comp_split) > 1:
            comp: str = comp_split[0].strip()
            jump: str = comp_split[1].strip()
        else:
            comp = comp_split[0].strip()
            jump = "null"

        valid: bool = (
            (dest in d_dict.keys())
            and (comp in c_dict.keys())
            and (jump in j_dict.keys())
        )

        return valid, c_dict.get(comp, ""), d_dict.get(dest, ""), j_dict.get(jump, "")

    def is_a_instruction(self, line: str) -> bool:
        return line.startswith("@")

    def first_pass(self) -> None:
        is_comment: bool = False
        line_count: int = 0
        for line in self.asm_lines:
            # filter multi-line comments
            if is_comment:
                comm_end: int = line.find("*/")
                if comm_end < 0:
                    continue
                else:
                    is_comment = False
                    line = line[comm_end + 2 :]
            else:
                comm_start: int = line.find("/*")
                if comm_start >= 0:
                    line = line[:comm_start]
            # filter inline comments
            hashtagpos: int = line.find("#")
            if hashtagpos >= 0:
                line = line[:hashtagpos]
            line = line.strip()
            # skip empty lines
            if not line:
                continue
            if line.startswith("("):
                label: str = line.removeprefix("(").removesuffix(")")
                self.st.add_symbol(label, line_count)
            elif self.is_a_instruction(line) or (self.is_c_instruction(line)[0]):
                line_count += 1
                self.asm_filtered.append(line)

    def second_pass(self) -> None:
        for line in self.asm_filtered:
            if self.is_a_instruction(line):
                line = line.removeprefix("@")
                if line.isnumeric():
                    self.instructions.append(Instruction(int(line)))
                else:
                    self.st.add_variable(line)
                    self.instructions.append(Instruction(self.st.get_symbol(line)))
            c_parse = self.is_c_instruction(line)
            if c_parse[0]:
                c, d, j = c_parse[1:]
                i = Instruction("111" + c + d + j)
                self.instructions.append(i)

    def parse(self, name: str) -> None:
        self.reset()
        self.read_asm(name)
        self.first_pass()
        self.second_pass()
        self.write_hack(name)
