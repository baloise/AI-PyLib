import itertools
import sys
import time
import threading

class Spinner:
    def __init__(self, message="Loading"):
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._spin)
        self.message = message

    def _spin(self):
        while not self.stop_event.is_set():
            sys.stdout.write(f'\r{self.message} {next(self.spinner)} ')
            sys.stdout.flush()
            time.sleep(0.2)

    def start(self):
        self.stop_event.clear()
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        sys.stdout.write(f'\r{self.message}  \n')
        self.thread.join()