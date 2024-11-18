from src.instruction import Instruction


class ALU:
    def __init__(self) -> None:
        self.result: Instruction = Instruction()
        self.isneg: bool = False
        self.is0: bool = True

    def clock(
        self,
        zx: bool,
        nx: bool,
        zy: bool,
        ny: bool,
        f: bool,
        no: bool,
        x: Instruction,
        y: Instruction,
    ) -> None:
        if zx:
            x = Instruction(0)
        if nx:
            x = ~x
        if zy:
            y = Instruction(0)
        if ny:
            y = ~y
        if f:
            self.result = x + y
        else:
            self.result = x & y
        if no:
            self.result = ~self.result

        self.isneg = self.result < 0
        self.is0 = self.result == 0
