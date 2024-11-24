from pathlib import Path
from src.vm.commands import Translator, bootstrap

valid_commands: dict[str, int] = {
    "push": 3,
    "pop": 3,
    "add": 1,
    "sub": 1,
    "neg": 1,
    "eq": 1,
    "gt": 1,
    "lt": 1,
    "and": 1,
    "or": 1,
    "not": 1,
    "label": 2,
    "goto": 2,
    "if-goto": 2,
    "function": 3,
    "call": 3,
    "return": 1,
}


class Parser:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.vm_lines: list[str] = []
        self.asm_lines: list[str] = bootstrap()

    def read_vm(self, file: Path) -> None:
        with file.open() as f:
            self.vm_lines = f.readlines()

    def write_asm(self, proj_name: str) -> None:
        path = Path("files/asm") / (proj_name + ".asm")
        with path.open("w") as f:
            f.writelines("\n".join(self.asm_lines))

    def parse_vm_line(self, line: str) -> list[str]:
        words: list[str] = line.strip().split()
        if len(words) == 0 or len(words) == 3 and not words[2].isnumeric():
            return []
        if len(words) != valid_commands.get(words[0], 0):
            return []
        return words

    def parse(self, source: str) -> None:
        self.reset()
        proj_name: str = ""
        files: list[Path] = []
        if (srcpath := Path(source)).is_dir():
            files = [file for file in srcpath.glob("*.vm")]
            proj_name = srcpath.name
        elif srcpath.is_file() and srcpath.suffix == ".vm":
            files = [srcpath]

        for file in files:
            classname: str = file.name.removesuffix(".vm")
            self.read_vm(file)
            tl = Translator(classname)
            for line in self.vm_lines:
                words: list[str] = self.parse_vm_line(line)
                self.asm_lines += tl.translate(words)
        if proj_name:
            self.write_asm(proj_name)
