import time
import re
from typing import TYPE_CHECKING

import aiohttp

from discordgsm.logger import Logger

from discordgsm.protocols.protocol import Protocol

if TYPE_CHECKING:
    from discordgsm.gamedig import GamedigResult


class HTTP(Protocol):
    name = "http"

    async def query(self):
        url, status_code, response_content, website_name = (
            str(self.kv["host"]),
            int(str(self.kv["status_code"])),
            str(self.kv["response_content"]),
            str(self.kv["website_name"]),
        )

        start = time.time()
        Logger.info(f"Querying {url} to check it its is online...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status
                content = await response.text()
                end = time.time()
                Logger.info(f"Finished check if {url} is online!")

        if not status == status_code:
            raise Exception(f"Received unexpected status code {status}")

        if not re.search(response_content, content):
            raise Exception("Response body did not match provided regex!")

        result: GamedigResult = {
            "name": website_name,
            "map": "",
            "password": False,
            "numplayers": 0,
            "numbots": 0,
            "maxplayers": -1,
            "players": None,
            "bots": None,
            "connect": f"{url}",
            "ping": int((end - start) * 1000),
            "raw": {
                status_code: status,
                response_content: content
            },
        }

        return result
