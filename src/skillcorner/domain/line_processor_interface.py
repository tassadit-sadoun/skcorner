from typing import Protocol


class ILineProcessor(Protocol):
    def process(self, line: str, line_number: int) -> str: ...
