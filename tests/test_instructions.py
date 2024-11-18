from src.instruction import Instruction, value_from_string, bound_value
import pytest


@pytest.mark.parametrize(
    "inp,out",
    [
        (0, 0),
        (1, 1),
        (-1, -1),
        (2**15, -(2**15)),
        (-(2**15) - 1, 2**15 - 1),
        (2**16, 0),
    ],
)
def test_bound_value(inp: int, out: int) -> None:
    assert bound_value(inp) == out


@pytest.mark.parametrize(
    "s,val", [("0", 0), ("1", 1), ("10101", 21), ("1111_1111_1111_1111", -1)]
)
def test_value_string(s: str, val: int) -> None:
    assert value_from_string(s) == val


def test_init() -> None:
    one = Instruction(1)
    one2 = Instruction("1")
    assert one == one2 == 1
    assert one == "0000_0000_0000_0001"


def test_neg() -> None:
    minusone = -Instruction(1)
    assert minusone == -1


def test_inv() -> None:
    assert ~Instruction() == -1


def test_add() -> None:
    assert Instruction(3) + Instruction(5) == 8


def test_and() -> None:
    assert Instruction(3) & Instruction(5) == Instruction(1)
