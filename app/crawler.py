#!/bin/python3
#
#       Crawl an entire site.
#

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
import math
import logging

if (len(sys.argv) != 2):
    print('Usage:'+sys.argv[0]+' http://example.com')

seed = sys.argv[1]
VIS = set()
ADD = lambda u: VIS.add(u) or u
IS_LOCAL_DOMAIN = lambda u: urlparse(seed).netloc == urlparse(u).netloc
NOT_MEDIA = lambda u: not re.compile(r'^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png|js|css|less|sass)$').match(u)
NOT_INDEXED = lambda u: u not in VIS
REQUESTS = 0
START_T = time.time()

def print_info():
    global START_T
    global REQUESTS
    REQUESTS += 1
    print("Time elapsed: ", math.floor((time.time()-START_T)))
    print("Links saved: ",len(VIS))
    print("Pages visited:c", REQUESTS)
    print("Requests/second: ",REQUESTS//(time.time()-START_T))

def is_ok(link):
    url = urljoin(seed, link)
    return NOT_MEDIA(url) and \
        IS_LOCAL_DOMAIN(url) and \
        NOT_INDEXED(url)

async def get(u,c, log):
    try:
        async with c.get(u) as response:
            page = await response.read()
        print_info()
        log("Visited: %s", u)
        soup = BeautifulSoup(page,'lxml').find_all('a')
        links  = [ADD(urljoin(seed, a.get('href')))
                  for a in soup if is_ok(a.get('href'))]
        if (links):
            asyncio.wait([asyncio.ensure_future(get(li, c, log)) for li in links])
    except Exception as e:
        log("error %s reason: %s" % (u, e))

def main():
    log = logging.getLogger().info
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    asyncio.wait(asyncio.ensure_future(get(seed, client, log)))
    loop.run_forever() # Right now it will never return from here.
    client.close()

# aiohttp.errors.ClientOSError:
if __name__ == '__main__':
    main()
