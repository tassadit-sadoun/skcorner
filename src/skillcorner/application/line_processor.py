import json

from skillcorner.domain.line_processor_interface import ILineProcessor


class DefaultLineProcessor(ILineProcessor):
    NOTHING = "Nothing to display"

    def process(self, line: str, line_number: int) -> str:

        # 1. multiple of 5
        if line_number % 5 == 0:
            return "Multiple of 5"

        # 2. contains $
        if "$" in line:
            return line.replace(" ", "_")

        # 3. ends with .
        if line.rstrip().endswith("."):
            return line.rstrip()

        # 4. JSON rule
        if line.startswith("{"):
            try:
                parsed = json.loads(line)

                if isinstance(parsed, dict):
                    parsed["even"] = line_number % 2 == 0
                    return json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))

            except json.JSONDecodeError:
                pass

        # 5. fallback
        return self.NOTHING
