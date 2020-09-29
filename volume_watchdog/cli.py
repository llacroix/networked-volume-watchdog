import asyncio

from .config import Config
from .watchdog import main_loop


def main(args=None, block=True):
    loop = asyncio.get_event_loop()
    config = Config()
    task = loop.create_task(main_loop(config))
    loop.run_until_complete(task)
