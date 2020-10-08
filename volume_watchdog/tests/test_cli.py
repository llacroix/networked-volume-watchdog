from volume_watchdog import cli
from volume_watchdog.watchdog import (
    get_device_path,
    get_full_path,
    get_path,
)


class Options(object):
    def __init__(self, regex, target):
        self.regex = regex
        self.target_path = target


def test_get_path():

    options = Options(":/gv0/(.*)", "/volumes")

    volume = {
        "Name": "test-base",
        "Options": {
            "type": "nfs",
            "device": ":/gv0/docker/volumes/test-base"
        }
    }

    rel_path = get_path(options, volume)
    assert rel_path == "docker/volumes/test-base"
    assert get_full_path(options, rel_path) == "/volumes/docker/volumes/test-base"

    volume2 = {
        "Name": "test-base2",
        "Options": {
            "type": "nfs"
        }
    }

    rel_path = get_path(options, volume2)
    assert rel_path == "test-base2"
    assert get_full_path(options, rel_path) == "/volumes/test-base2"

    volume3 = {
        "Name": "test-base",
        "Options": {
            "device": "nfs"
        }
    }

    assert get_path(options, volume3) is None

    options = Options(":/(.*)", "/volumes")

    volume = {
        "Name": "test-base",
        "Options": {
            "type": "nfs",
            "device": ":/gv0/docker/volumes/test-base"
        }
    }

    rel_path = get_path(options, volume)
    assert rel_path == "gv0/docker/volumes/test-base"
    assert get_device_path(options, volume.get('Options').get('device')) == "gv0/docker/volumes/test-base"
    assert get_full_path(options, rel_path) == "/volumes/gv0/docker/volumes/test-base"


    options = Options(":/", "/volumes")
    volume = {
        "Name": "test-base",
        "Options": {
            "type": "nfs",
            "device": ":/gv0/docker/volumes/test-base"
        }
    }

    assert get_path(options, volume) is None
