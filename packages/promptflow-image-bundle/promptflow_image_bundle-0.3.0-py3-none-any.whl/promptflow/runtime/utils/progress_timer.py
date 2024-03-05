import contextvars
import logging
import threading
import time
from time import perf_counter

from promptflow._internal import set_context


class ProgressTimer:
    def __init__(self, logger: logging.Logger, funcDescription: str, log_interval: float = 60):
        # bool in python is thread safe
        self.finish = False
        self.log_interval = log_interval

        self.logger = logger
        self.funcDescription = funcDescription
        self.start = None
        self.end = None
        self._context = contextvars.copy_context()

    def __enter__(self):
        self.start = perf_counter()
        progress_thread = threading.Thread(target=self.progress)
        progress_thread.start()
        return self

    def __exit__(self, *args):
        self.finish = True
        self.end = perf_counter()
        self.logger.info(f"{self.funcDescription} finished in {self.end - self.start} seconds")

    def progress(self):
        # set context for logging
        set_context(self._context)

        while not self.finish:
            time.sleep(self.log_interval)
            if self.finish:
                break  # avoid logging after exit
            self.logger.info(f"{self.funcDescription} is progressing")
