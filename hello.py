from src.assembler.parser import Parser as Assembler
from src.vm.parser import Parser as VMTranslator
from src.simulator.cpu import CPU


def pipeline(file: str) -> None:
    vmt = VMTranslator()
    vmt.parse(file)
    ass = Assembler()
    ass.parse(file)
    cpu = CPU()
    cpu.load_program(file)
    cpu.run()


if __name__ == "__main__":
    pipeline("test_1")
