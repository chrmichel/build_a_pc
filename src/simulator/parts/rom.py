from src.instruction import Instruction
from pathlib import Path


class ROM:
    def __init__(self) -> None:
        self.instructions: list[Instruction] = []
        self.length: int = 0

    def load_instructions(self, filename: str) -> None:
        filepath: Path = Path("files/hack/") / (filename + ".hack")
        with filepath.open() as f:
            lines: list[str] = f.readlines()
        for line in lines:
            try:
                instr: Instruction = Instruction(line)
            except Exception:
                continue
            self.instructions.append(instr)
        self.length = len(self.instructions)

    def get_instruction(self, number: int) -> tuple[bool, Instruction]:
        if 0 <= number < self.length:
            return True, self.instructions[number]
        else:
            return False, Instruction()
