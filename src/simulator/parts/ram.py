from src.instruction import Instruction

defaultdict: dict[int, int] = {}


class RAM:
    def __init__(self) -> None:
        self.data = defaultdict.copy()

    def __getitem__(self, addr: Instruction) -> Instruction:
        return Instruction(self.data.get(addr.value, 0))

    def __setitem__(self, addr: Instruction, val: Instruction) -> None:
        self.data[addr.value] = val.value

    def reset(self) -> None:
        self.data = defaultdict.copy()
