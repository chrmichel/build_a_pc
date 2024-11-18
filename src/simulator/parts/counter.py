class Counter:
    def __init__(self) -> None:
        self.count: int = 0

    def clock(self, val: int, jump: bool) -> int:
        if jump:
            self.count = val
        else:
            self.count += 1
        return self.count

    def reset(self) -> None:
        self.count = 0
