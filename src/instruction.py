from typing import Self


def bound_value(val: int) -> int:
    while val >= 2**15:
        val = val - 2**16
    while val < -(2**15):
        val += 2**16

    return val


def value_from_string(s: str) -> int:
    s = s.strip().replace(" ", "").replace("_", "")
    try:
        val: int = int(s, 2)
    except ValueError as v:
        raise v

    return bound_value(val)


class Instruction:
    def __init__(self, value: int | str | Self = 0) -> None:
        if isinstance(value, int):
            self._val: int = bound_value(value)
        elif isinstance(value, str):
            self._val: int = value_from_string(value)
        else:
            self._val: int = value._val

    def __str__(self) -> str:
        val: int = self._val
        if val < 0:
            val += 2**16
        return f"{val:016b}"

    @property
    def value(self) -> int:
        return self._val

    @value.setter
    def value(self, val: int | str) -> None:
        if isinstance(val, int):
            self._val = bound_value(val)
        else:
            self._val = value_from_string(val)

    def __add__(self, other: int | Self) -> Self:
        if isinstance(other, int):
            return type(self)(self.value + other)
        else:
            return type(self)(self.value + other.value)

    def __sub__(self, other: int | Self) -> Self:
        if isinstance(other, int):
            return type(self)(self.value - other)
        else:
            return type(self)(self.value - other.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            return str(self) == other.strip().replace(" ", "").replace("_", "")
        elif isinstance(other, type(self)):
            return self.value == other.value
        else:
            return NotImplemented

    def __and__(self, other: int | Self) -> Self:
        if isinstance(other, int):
            return type(self)(self.value & other)
        else:
            return type(self)(self.value & other.value)

    def __neg__(self) -> Self:
        return type(self)(-self.value)

    def __invert__(self) -> Self:
        return type(self)(-self.value - 1)

    def __lt__(self, other: int | Self) -> bool:
        if isinstance(other, int):
            return self.value < other
        else:
            return self.value < other.value

    def __gt__(self, other: int | Self) -> bool:
        if isinstance(other, int):
            return self.value > other
        else:
            return self.value > other.value

    def __le__(self, other: int | Self) -> bool:
        if isinstance(other, int):
            return self.value <= other
        else:
            return self.value <= other.value

    def __ge__(self, other: int | Self) -> bool:
        if isinstance(other, int):
            return self.value >= other
        else:
            return self.value >= other.value


if __name__ == "__main__":
    three = Instruction(3)
    print(three)

    assert three == "0000_0000_0000_0011"
