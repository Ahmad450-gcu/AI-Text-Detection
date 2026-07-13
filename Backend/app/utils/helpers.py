import time
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def timer() -> Iterator[dict]:
    start = time.perf_counter()
    result: dict = {"elapsed_ms": None}
    try:
        yield result
    finally:
        result["elapsed_ms"] = (time.perf_counter() - start) * 1000
