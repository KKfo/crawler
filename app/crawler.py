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
import time

SEED = sys.argv[1]
VIS = set()
ADD = lambda u: VIS.add(u) or u
URL = sys.argv[1]
IS_LOCAL_DOMAIN = lambda u: urlparse(URL).netloc == urlparse(u).netloc
NOT_MEDIA = lambda u: not re.compile(r'^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png|js|css|less|sass)$').match(u)
NOT_INDEXED = lambda u: u not in VIS
queue = []
REQUESTS = 0
START_T = time.time()
f = lambda A, n=50: [A[i:i+n] for i in range(0, len(A), n)]

async def get(u,c):
    async with c.get(u) as response:
        page = await response.read()
    global queue
    global START_T
    global REQUESTS
    REQUESTS += 1
    print("Pages visited:c", REQUESTS)
    print("Requests per second: ",REQUESTS/(time.time()-START_T))
    print("Links saved: ",len(VIS))
    soup = BeautifulSoup(page,'lxml').find_all('a')
    links  = [
        ADD(urljoin(URL, link.get('href'))) for link in soup  if 
        NOT_MEDIA(urljoin(URL, link.get('href'))) and
        IS_LOCAL_DOMAIN(urljoin(URL, link.get('href'))) and
        NOT_INDEXED(urljoin(URL, link.get('href')))]
    if (links):
        asyncio.wait([asyncio.ensure_future(get(li, c)) for li in links])

def main():
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    asyncio.wait(asyncio.ensure_future(get(SEED, client)))
    loop.run_forever()
    client.close()

# aiohttp.errors.ClientOSError:
if __name__ == '__main__':
    main()
