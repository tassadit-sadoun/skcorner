import logging
import sys
import time
from multiprocessing import cpu_count
from pathlib import Path

from skillcorner.application.line_processor import DefaultLineProcessor
from skillcorner.infrastructure.executor import StreamingExecutor

MIN_SIZE = 10 * 1024 * 1024


class Metrics:
    def __init__(self):
        self.processed = 0
        self.failed = 0

    def inc_processed(self):
        self.processed += 1

    def inc_failed(self):
        self.failed += 1


metrics = Metrics()


def should_use_multiprocess(file_path: str, user_enabled: bool) -> bool:
    if cpu_count() <= 1:
        return False

    path = Path(file_path)

    return user_enabled or (path.is_file() and path.stat().st_size >= MIN_SIZE)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    file_path = sys.argv[1]
    path = Path(file_path)

    # =========================================================
    # INPUT VALIDATION
    # =========================================================
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if not file_path.lower().endswith(".log"):
        raise ValueError(f"Invalid file type: {file_path}")

    user_flag = "--multiprocess" in sys.argv
    use_mp = should_use_multiprocess(file_path, user_flag)

    processor = DefaultLineProcessor()
    executor = StreamingExecutor(use_mp)

    logging.info(
        "starting processing file=%s multiprocess=%s",
        file_path,
        use_mp,
    )

    start = time.perf_counter()

    # =========================================================
    # EXECUTION
    # =========================================================
    try:
        with path.open(encoding="utf-8", buffering=1024 * 1024) as f:
            for result in executor.run(processor, f):
                sys.stdout.write(f"{result.line_number} : {result.value}\n")

                if result.value == "ERROR_PROCESSING_LINE":
                    metrics.inc_failed()
                else:
                    metrics.inc_processed()

    except Exception as e:
        logging.error("processing failed: %s", e)
        sys.exit(1)

    # =========================================================
    # METRICS
    # =========================================================
    duration = time.perf_counter() - start

    if duration > 0:
        logging.info(
            "processed=%d failed=%d throughput=%.2f lines/sec",
            metrics.processed,
            metrics.failed,
            metrics.processed / duration,
        )


if __name__ == "__main__":
    main()
