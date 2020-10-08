import asyncio
import logging
from os import path
import os
import re

logger = logging.getLogger(__name__)


def get_device_path(options, device):
    try:
        regex = re.compile(options.regex)
        match = regex.match(device)
        if match:
            return match.group(1)
    except Exception:
        return


def get_path(options, volume):
    opts = volume.get('Options', {})
    if opts and opts.get('type') == 'nfs':
        if opts.get('device') and options.regex:
            return get_device_path(options, opts.get('device'))
        else:
            return volume['Name']


def ensure_directory(options, target_path):
    """
    Ensure a directory exist based on the target path
    """
    try:
        # TODO create the path tree instead of expecting the last subdirectory
        # to actually exist
        if not path.exists(target_path):
            logger.info(
                "Target path %s doesn't exist" % (target_path,)
            )
            os.mkdir(target_path)
    except Exception:
        logger.info("Couldn't create path %s" % (target_path,), exc_info=True)


def get_full_path(options, relative_path):
    local_path = options.target_path
    target_path = path.join(local_path, relative_path)
    return target_path


async def listen_events(config):
    """
    Listen for events and recreate the config whenever a container start/stop
    """
    docker = config.get_client()
    subscriber = docker.events.subscribe()

    logger.info("Listening for docker events")

    try:
        while True:
            logger.info("Waiting for event")
            event = await subscriber.get()
            if event and event.get('Type') == 'volume':
                volumes = await docker.volumes.list()

                for volume in volumes.get('Volumes', []):
                    if volume.get('Name') in config.options.ignores:
                        continue

                    relative_path = get_path(config.options, volume)
                    if not relative_path:
                        continue

                    target_path = get_full_path(config.options, relative_path)

                    if not path.exists(target_path):
                        ensure_directory(config.options, target_path)

    except Exception:
        logger.info("Something wrong happened", exc_info=True)
        raise


async def main_loop(config):
    loop = asyncio.get_event_loop()
    while True:
        read_events_task = loop.create_task(listen_events(config))
        done, pending = await asyncio.wait(
            [read_events_task]
        )
