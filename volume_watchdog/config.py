import aiodocker
import logging
import sys


class Options(object):
    def __init__(self):
        self.host = 'unix:///var/run/docker.sock'
        self.target_path = "/data/gluster/docker/volumes"
        self.log_level = "INFO"
        self.log_file = None


class Config(object):
    def __init__(self, args=None, docker_client=aiodocker.Docker):
        self.docker_client = docker_client
        self.inited = False
        self.options = Options()

    def init(self):
        self.docker = self.docker_client(url=self.options.host)
        self.inited = True

    async def deinit(self):
        await self.docker.close()
        self.inited = False

    def get_client(self):
        if not self.inited:
            self.init()
        return self.docker


def setup_logging(config):
    options = config.options

    level = logging.getLevelName(options.log_level)
    logger = logging.getLogger('')
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not options.log_file:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(options.log_file)

    handler.setFormatter(formatter)

    config.log_handler = handler

    logger.addHandler(handler)

    logger.info('Logging enabled')
