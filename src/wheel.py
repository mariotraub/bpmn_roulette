from enum import Enum
from random import randint
from typing import override

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLACK = "black"


class Result:
    def __init__(self, num: int, color: Color, is_even: bool):
        self.num: int = num
        self.color: Color = color
        self.is_even: bool = is_even
    @override
    def __str__(self):
        return f"num: {self.num}, color: {self.color}, is_even: {self.is_even}"


red_numbers = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}


def spin() -> Result:
    num = randint(0, 36)    
    if num == 0:
        color = Color.GREEN
    elif num in red_numbers:
        color = Color.RED
    else:
        color = Color.BLACK

    is_even = num % 2 == 0

    return Result(num, color, is_even)
