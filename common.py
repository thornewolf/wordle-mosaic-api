from dataclasses import dataclass
from enum import Enum


@dataclass
class Resolution:
    width: int
    height: int


class WordleSquare(Enum):
    GREEN = "🟩"
    YELLOW = "🟨"
    BLACK = "⬛"
    WHITE = "⬜"
