import time
import logging


class Logger:
    def __init__(self):
        logging.basicConfig(filename="SupportBank.log", filemode="w", level=logging.DEBUG)

    @staticmethod
    def fail(message):
        current_time = time.ctime()
        logging.info(f"[{current_time}] {message}")
        print(f"[{current_time}] {message}")
