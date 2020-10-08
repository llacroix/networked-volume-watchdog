import asyncio

from .config import Config, setup_logging
from .watchdog import main_loop
from optparse import OptionParser
import sys

from logging import getLogger

logger = getLogger(__name__)
docker_url = "unix:///var/run/docker.sock"


def get_parser():
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--directory",
        dest="target_path",
        help="Directory in which the volumes are created",
    )

    parser.add_option(
        "-r",
        "--regex-path",
        dest="regex",
        help="Regex to extract the path where the mounted directory is located"
    )

    parser.add_option("--log-level", dest="log_level", default="INFO")
    parser.add_option("--log-file", dest="log_file", default=None)
    parser.add_option(
        "--host", dest="host", default=docker_url, help="Docker Host/Socket",
    )
    return parser


def main(args=None, block=True):
    loop = asyncio.get_event_loop()
    config = Config()
    parser = get_parser()
    (options, args) = parser.parse_args(
        args if args is not None else sys.argv[1:]
    )
    config.options = options
    setup_logging(config)
    logger.info("Starting up %s", args)
    logger.info("Volumes directory will be created in %s", options.target_path)
    task = loop.create_task(main_loop(config))

    if block:
        loop.run_until_complete(task)
