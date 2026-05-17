# ⚡ Log Processing

A streaming system that processes log files line-by-line using a rule-based processor with optional multiprocessing execution.


## 🧠 Core behavior

Each line is transformed using the first matching rule:

- LINE_NUMBER % 5 == 0 → "Multiple of 5"
- Contains `$` → replace spaces with `_`
- Ends with `.` → return trimmed original line
- Starts with `{` → JSON parse + add `"even"` flag
- Otherwise → "Nothing to display"

Only the first matching rule applies.

---

# 🏗 Architecture

- **Executor**: streaming execution layer handling both sequential and multiprocessing strategies.
- **Processor**: stateless domain component implementing line transformation rules.
- **main**: composition root responsible for CLI, runtime configuration, wiring, and logging.

---

# ⚙️ Execution Model

## Single-process
- Sequential streaming
- Deterministic ordering
- Low overhead execution path

## Multiprocessing
- `multiprocessing.Pool`
- `imap_unordered`
- Chunked scheduling (`chunksize`)

---

# 🧠 Design Principles

- **Streaming-first**: processes input incrementally without full file materialization
- **Stateless processing**: each line is independent and safely parallelizable
- **Explicit concurrency boundary**: multiprocessing isolated in infrastructure layer
- **Failure isolation**: processing errors mapped to explicit sentinel results (no pipeline crash)
- **Minimal abstraction surface**: avoids unnecessary layering complexity
- **Separation of concerns**:
  - execution & concurrency → infrastructure layer
  - business rules → domain layer
  - wiring & runtime config → entrypoint


# 📁 Structure

```text
src/skillcorner/
├── app/                        → Entry point
│   ├── main.py
│
│
├── application/               → Application logic (line processing rules)
│   └── line_processor.py     →  Rule-based line processing engine 
│
├── domain/                    → Core contracts (business interfaces only)
│   └── line_processor_interface.py
        entities.py              → Domain entities (e.g. LineResult)
│
├── infrastructure/            → Execution engine (I/O, streaming, multiprocessing)
│   └── executor.py
│
└── tests/                     → Test strategy by architectural layer
    ├── domain/                → Unit tests for line processing rules
    ├── infrastructure/        → Behavioral tests for execution engine
```
---

# Execution

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```
## Run tests
```bash
pytest -q
```
## Lint and type check
```bash
ruff check .
ruff format --check .
ruff format .
mypy src
```

## 🚀 Usage

The application runs in two modes depending on workload size or user input.

### Single-process mode (default)

Executes the pipeline in a single process. Used for small files or when multiprocessing is disabled.

```bash
python src/skillcorner/app/main.py data.log
```

### Multiprocessing mode

Uses multiple processes to parallelize line processing. Enabled manually or automatically for large inputs.
```bash

python src/skillcorner/app/main.py data.log --multiprocess
```
### Large dataset testing:

A helper script can be used to generate large input files for performance testing:
bash

python scripts/generate_big_file.py
---


### Testing Strategy

- **Processor (application layer)**: deterministic unit tests covering rule evaluation, precedence, and output contract for each transformation case.
- **Executor (infrastructure layer)**:behavioral tests validating streaming correctness, execution consistency, concurrency modes, and line-level error isolation, with ordering guarantees in single-process and relaxed ordering in multiprocess.

### CI Design Choice

The CI pipeline is designed as a strict quality gate per layer: **build, lint, and tests** 
are fully separated into independent jobs.
This choice enforces **early failure detection**,
ensuring that no unvalidated code reaches the main branch.

## 📡 Observability

The system exposes a minimal, structured observability layer based on batch-level logging.

### 📊 Example log output

```text
2026-05-17 20:55:50,178 | INFO | skillcorner.infrastructure.executor | StreamingExecutor initialized mode=multiprocess
2026-05-17 20:55:50,178 | INFO | root | starting processing file=huge_data.log multiprocess=True
2026-05-17 20:55:50,243 | INFO | root | starting multiprocessing pool workers=7
2026-05-17 20:55:54,124 | INFO | root | processed=1000000 failed=0 throughput=61026.19 lines/sec