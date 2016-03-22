# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para flashx
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand/
# ------------------------------------------------------------

import re
import urllib

from core import jsunpack
from core import logger
from core import scrapertools

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate']
]


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("streamondemand.servers.flashx url=" + page_url)

    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    page_url = scrapertools.find_single_match(data, 'href="([^"]+)')

    if page_url:
        data = scrapertools.cache_page(page_url, headers=headers)

    data = scrapertools.find_single_match(data, '(eval\(function.*?)</script>')

    if data:
        data = jsunpack.unpack(data)
        _headers = urllib.urlencode(dict(headers))

        # Extrae la URL
        media_urls = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"')
        for media_url in media_urls:
            if not media_url.endswith("png"):
                video_urls.append([media_url[-4:] + " [flashx]", media_url + '|' + _headers])

        for video_url in video_urls:
            logger.info("streamondemand.servers.flashx %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'flashx.(?:tv|pw)/(?:embed-|)([a-z0-9A-Z]+)'
    logger.info("streamondemand.servers.flashx find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "http://www.flashx.pw/embed.php?c=%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'flashx'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
