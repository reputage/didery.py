import arrow
import asyncio
import aiohttp

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping as h


async def httpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            print(data)
            return data


async def httpPost(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=data, headers=headers) as response:
            status = response.status
            data = await response.text()

            return status, data


def getHistory(url, did):
    pass


def postHistory(url, data, sk):
    pass


def putHistory(url, did, data, sk, psk):
    pass
