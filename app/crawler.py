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

links = [sys.argv[1]]
VIS = set()
ADD = lambda u: VIS.add(u) or u
URL = sys.argv[1]
IS_LOCAL_DOMAIN = lambda u: urlparse(URL).netloc == urlparse(u).netloc
NOT_MEDIA = lambda u: not re.compile(r'^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png|js|css|less|sass)$').match(u)
NOT_INDEXED = lambda u: u not in VIS
queue = []
f = lambda A, n=1: [A[i:i+n] for i in range(0, len(A), n)]
async def get(urls):
    pages = []
    for u in urls:
        async with aiohttp.get(u) as response:
            pages.append(await response.read())
    soups = [BeautifulSoup(page, 'lxml').find_all('a') for page in pages]
    links  = [
        ADD(urljoin(URL, link.get('href'))) for SOUP in soups for link in SOUP  if 
        NOT_MEDIA(urljoin(URL, link.get('href'))) and
        IS_LOCAL_DOMAIN(urljoin(URL, link.get('href'))) and
        NOT_INDEXED(urljoin(URL, link.get('href')))]
    print(len(VIS))
    if (links):
        splited = f(links)
        asyncio.wait([asyncio.ensure_future(get(li)) for li in splited])

def main():
    loop = asyncio.get_event_loop()
    asyncio.wait(asyncio.ensure_future(get(links)))
    loop.run_forever()

# aiohttp.errors.ClientOSError:
if __name__ == '__main__':
    main()
