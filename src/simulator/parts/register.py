from src.instruction import Instruction


class Register:
    def __init__(self) -> None:
        self.value: Instruction = Instruction()
        self.next: Instruction = Instruction()

    def clock(self) -> None:
        self.value = self.next

    def reset(self) -> None:
        self.value = Instruction()
        self.next = Instruction()
