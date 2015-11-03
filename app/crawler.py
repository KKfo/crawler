#!/bin/python3
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import asyncio_redis
from urllib.parse import urlparse, urljoin
import sys
import re
import codecs
import math

SEED = sys.argv[1]
VIS = set()
ADD = lambda u: VIS.add(u) or u
URL = sys.argv[1]
IS_LOCAL_DOMAIN = lambda u: urlparse(URL).netloc == urlparse(u).netloc
NOT_MEDIA = lambda u: not re.compile(r'^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png|js|css|less|sass)$').match(u)
NOT_INDEXED = lambda u: u not in VIS
queue = []
async def get(u):
    async with aiohttp.get(u) as response:
         page = await response.read()
    global queue
    soup = BeautifulSoup(page,'lxml').find_all('a')
    links  = [
        ADD(urljoin(URL, link.get('href'))) for link in soup  if 
        NOT_MEDIA(urljoin(URL, link.get('href'))) and
        IS_LOCAL_DOMAIN(urljoin(URL, link.get('href'))) and
        NOT_INDEXED(urljoin(URL, link.get('href')))]
    print(len(VIS))
    if (links):
        queue += [asyncio.ensure_future(get(li)) for li in links]
        if (len(queue) > 1000):
            asyncio.wait(queue)
            queue = []

def main():
    loop = asyncio.get_event_loop()
    asyncio.wait(asyncio.ensure_future(get(SEED)))
    loop.run_forever()

# aiohttp.errors.ClientOSError:
if __name__ == '__main__':
    main()
