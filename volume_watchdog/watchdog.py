import asyncio
import logging
from os import path
import os

logger = logging.getLogger(__name__)


async def listen_events(config):
    """
    Listen for events and recreate the config whenever a container start/stop
    """
    docker = config.get_client()
    subscriber = docker.events.subscribe()

    logger.info("Listening for docker events")

    local_path = config.options.target_path

    try:
        while True:
            logger.info("Waiting for event")
            event = await subscriber.get()
            if event.get('Type') == 'volume':
                volume_id = event['Actor']['ID']
                volumes = await docker.volumes.list()
                for volume in volumes.get('Volumes', []):
                    if volume['Options'].get('type') == 'nfs':
                        target_path = path.join(local_path, volume_id)

                        if not path.exists(target_path):
                            logger.info(
                                "Target path %s doesn't exist" % (target_path,)
                            )
                            os.mkdir(target_path)

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
