# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para thevideo.me
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("streamondemand.servers.thevideome url=" + page_url)

    data = scrapertools.cache_page(page_url)
    media_urls = scrapertools.find_multiple_matches(data, r"'?label'?\s*:\s*'([^']+)p'\s*,\s*'?file'?\s*:\s*'([^']+)")
    video_urls = []

    for label, media_url in media_urls:
        video_urls.append(
            [scrapertools.get_filename_from_url(media_url)[-4:] + " (" + label + ") [thevideo.me]", media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = ['thevideo.me/embed-([a-z0-9A-Z]+)',
                    'thevideo.me/([a-z0-9A-Z]+)']
    for patron in patronvideos:
        logger.info("streamondemand.servers.thevideome find_videos #" + patron + "#")
        matches = re.compile(patron, re.DOTALL).findall(data)

        for match in matches:
            titulo = "[thevideo.me]"
            url = "http://thevideo.me/embed-" + match + ".html"
            if url not in encontrados:
                logger.info("  url=" + url)
                devuelve.append([titulo, url, 'thevideome'])
                encontrados.add(url)
            else:
                logger.info("  url duplicada=" + url)
    return devuelve
