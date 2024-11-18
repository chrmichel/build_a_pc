from src.simulator.parts.alu import ALU
from src.simulator.parts.counter import Counter
from src.simulator.parts.ram import RAM
from src.simulator.parts.register import Register
from src.simulator.parts.rom import ROM

from src.instruction import Instruction


class CPU:
    def __init__(self) -> None:
        self.counter = Counter()
        self.alu = ALU()
        self.a_reg = Register()
        self.d_reg = Register()
        self.ram = RAM()
        self.rom = ROM()

        self.jump: bool = False

    def load_program(self, filename: str) -> None:
        self.rom.load_instructions(filename)
        self.counter.reset()
        self.a_reg.reset()
        self.d_reg.reset()
        self.ram.reset()

    def run(self) -> None:
        running, instr = self.rom.get_instruction(0)
        while running:
            next_line: int = self.clock(instr)
            running, instr = self.rom.get_instruction(next_line)
        print(self.ram.data)

    def clock(self, ins: Instruction) -> int:
        is_a_instruction: bool = ins >= 0
        if is_a_instruction:
            self.a_reg.next = ins
            jump: bool = False
        else:
            use_m, zx, nx, zy, ny, f, no, a, d, m, j1, j2, j3 = (
                self.parse_c_instruction(ins)
            )
            a_value: Instruction = (
                self.ram[self.a_reg.value] if use_m else self.a_reg.value
            )
            d_value: Instruction = self.d_reg.value
            self.alu.clock(zx, nx, zy, ny, f, no, d_value, a_value)
            if m:
                self.ram[self.a_reg.value] = self.alu.result
            if d:
                self.d_reg.next = self.alu.result
            if a:
                self.a_reg.next = self.alu.result
            jump: bool = (
                (j3 and not self.alu.isneg and not self.alu.is0)
                or (j2 and self.alu.is0)
                or (j1 and self.alu.isneg)
            )
        self.a_reg.clock()
        self.d_reg.clock()
        return self.counter.clock(self.a_reg.value.value, jump)

    def parse_c_instruction(self, ins: Instruction) -> list[bool]:
        return [True if bit == "1" else False for bit in str(ins)[3:]]


if __name__ == "__main__":
    pass
