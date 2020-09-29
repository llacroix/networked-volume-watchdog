import aiodocker


class Options(object):
    def __init__(self):
        self.host = 'unix:///var/run/docker.sock'
        self.target_path = "/data/gluster/docker/volumes"


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
