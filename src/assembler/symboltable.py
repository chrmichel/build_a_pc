def defaultdict() -> dict[str, int]:
    default = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }
    for i in range(16):
        default[f"R{i}"] = i
    return default


class SymbolTable:
    def __init__(self) -> None:
        self.data = defaultdict()
        self.var_counter: int = 0

    def contains(self, symbol: str) -> bool:
        return symbol in self.data.keys()

    def add_symbol(self, symbol: str, value: int) -> None:
        self.data[symbol] = value

    def add_variable(self, name: str) -> None:
        if not self.contains(name):
            self.var_counter += 1
            self.add_symbol(name, self.var_counter + 15)

    def get_symbol(self, symbol: str) -> int:
        return self.data.get(symbol, 0)
