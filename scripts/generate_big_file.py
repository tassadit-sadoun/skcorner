import random
from pathlib import Path

OUTPUT_FILE = Path("huge_data.log")
NUMBER_OF_LINES = 1_000_000


# ==========================================================
# DATASETS
# ==========================================================

JSON_LINES = [
    '{"player": {"first_name": "Sergio", "last_name": "Ramos", "Age": 34},'
    ' "team": "Real Madrid"}',
    '{"player": {"first_name": "Kylian", "last_name": "Mbappé", "Age": 22},'
    ' "team": "PSG"}',
    '{"player": {"first_name": "Edinson", "last_name": "Cavani", "Age": 33},'
    ' "team": "Manchester United"}',
    '{"player": {"first_name": "Harry", "last_name": "Kane", "Age": 27},'
    ' "team": "Tottenham"}',
    '{"player": {"first_name": "Luis", "last_name": "Suárez", "Age": 34},'
    ' "team": "Atlético Madrid"}',
    '{"player": {"first_name": "Jamie", "last_name": "Vardy", "Age": 34},'
    ' "team": "Leicester"}',
]

TEXT_LINES = [
    "Match 756 has started",
    "Process 5828 succesfully run",
    "Process 222 succesfully run",
    "Process 9000 suc$esfully run",
    "Process 4758 succesfully run",
    "Match 3341 has finished",
    "Match 444 has fin#shed",
    "Match 95687 has fin$shed",
    'Process 3300" succesfully run',
    "Error during match 90206",
    "Process 498758 succesfully run.",
]


# ==========================================================
# GENERATION
# ==========================================================

ALL_LINES = JSON_LINES + TEXT_LINES

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    for _ in range(NUMBER_OF_LINES):
        line = random.choice(ALL_LINES)
        file.write(line + "\n")


print(f"Generated: {OUTPUT_FILE}")
