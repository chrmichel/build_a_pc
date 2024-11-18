from src.assembler.parser import Parser as Assembler
from src.simulator.cpu import CPU


def pipeline(file: str) -> None:
    ass = Assembler()
    ass.parse(file)
    cpu = CPU()
    cpu.load_program(file)
    cpu.run()


if __name__ == "__main__":
    pipeline("test_sum")
