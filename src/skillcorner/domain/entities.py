from dataclasses import dataclass


@dataclass(frozen=True)
class LineResult:
    line_number: int
    value: str
