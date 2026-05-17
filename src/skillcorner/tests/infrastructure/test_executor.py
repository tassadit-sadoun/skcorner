from io import StringIO

import pytest

from skillcorner.infrastructure.executor import StreamingExecutor

# ==========================================================
# TEST DOUBLES
# ==========================================================


class FakeProcessor:
    def process(self, line: str, line_number: int) -> str:
        return line.upper()


class FailingProcessor:
    def process(self, line: str, line_number: int) -> str:
        raise RuntimeError("boom")


# ==========================================================
# HELPERS
# ==========================================================


def make_stream(data: str) -> StringIO:
    return StringIO(data)


def run_executor(processor, data: str, multiprocess: bool):
    executor = StreamingExecutor(use_multiprocess=multiprocess)
    stream = make_stream(data)

    return list(executor.run(processor, stream))


# ==========================================================
# CORE EXECUTION FLOW
# ==========================================================


@pytest.mark.parametrize("multiprocess", [False, True])
def test_executor_processes_lines(multiprocess):
    results = run_executor(
        FakeProcessor(),
        "a\nb\nc\n",
        multiprocess,
    )

    assert [r.value for r in results] == ["A\n", "B\n", "C\n"]


# ==========================================================
# ORDER GUARANTEE (single process only)
# ==========================================================


def test_single_process_preserves_order():
    results = run_executor(
        FakeProcessor(),
        "a\nb\nc\n",
        multiprocess=False,
    )

    assert [r.line_number for r in results] == [0, 1, 2]


# ==========================================================
# ERROR HANDLING
# ==========================================================


@pytest.mark.parametrize("multiprocess", [False, True])
def test_executor_handles_processing_errors(multiprocess):
    results = run_executor(
        FailingProcessor(),
        "a\n",
        multiprocess,
    )

    assert results[0].value == "ERROR_PROCESSING_LINE"
