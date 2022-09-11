import sys
from datetime import datetime


class Logger:
    def __init__(self, debug_mode=False, log_stream=sys.stdout, error_stream=sys.stderr, debug_stream=sys.stdout):
        self.debug_mode = debug_mode
        self.log_stream = log_stream
        self.error_stream = error_stream
        self.debug_stream = debug_stream

    def log(self, message):
        print(message, file=self.log_stream)

    def error(self, message):
        print(f"[{datetime.now()}] [ERROR] {message}", file=self.error_stream)

    def debug(self, message):
        if self.debug_mode:
            print(f"[{datetime.now()}] [DEBUG] {message}", file=self.debug_stream)
