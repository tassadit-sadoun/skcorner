import logging
from collections.abc import Callable, Iterator
from functools import partial
from multiprocessing import Pool, cpu_count
from typing import TextIO

from skillcorner.application.line_processor import ILineProcessor
from skillcorner.domain.entities import LineResult

ProcessFn = Callable[[tuple[int, str]], LineResult]


def process_line(
    processor: ILineProcessor,
    item: tuple[int, str],
) -> LineResult:
    i, line = item

    try:
        value = processor.process(line, i)
        return LineResult(i, value)

    except Exception:
        return LineResult(i, "ERROR_PROCESSING_LINE")


logger = logging.getLogger(__name__)


class StreamingExecutor:
    def __init__(
        self,
        use_multiprocess: bool,
    ):
        self.use_multiprocess = use_multiprocess

        logger.info(
            "StreamingExecutor initialized mode=%s",
            "multiprocess" if use_multiprocess else "single",
        )

    def _run_single(
        self, process: ProcessFn, file_object: TextIO
    ) -> Iterator[LineResult]:

        yield from map(process, enumerate(file_object))

    def _run_multi(
        self, process: ProcessFn, file_object: TextIO
    ) -> Iterator[LineResult]:
        workers = max(1, cpu_count() - 1)
        with Pool(workers) as pool:
            logging.info(
                "starting multiprocessing pool workers=%d",
                workers,
            )
            yield from pool.imap_unordered(
                process,
                enumerate(file_object),
                chunksize=3000,
            )

    def run(
        self,
        processor: ILineProcessor,
        file_object: TextIO,
    ) -> Iterator[LineResult]:

        if not file_object:
            raise ValueError("file_object must be a valid file-like object")

        logging.info(
            "executor run started multiprocess=%s",
            self.use_multiprocess,
        )

        process = partial(process_line, processor)

        runner = self._run_multi if self.use_multiprocess else self._run_single

        yield from runner(process, file_object)
