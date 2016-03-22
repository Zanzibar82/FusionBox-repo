# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Server per youwatch
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import jsunpack
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("youwatch test_video_exists(page_url='%s')" % page_url)
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("youwatch get_video_url(page_url='%s')" % page_url)

    data = ''
    patron_new_url = '<iframe[^>]*src="([^"]+/embed[^"]+)'

    while page_url != "":
        headers = [
            ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0'],
            ['Accept-Encoding', 'gzip, deflate'],
            ['Referer', page_url]
        ]
        data = scrapertools.cache_page(page_url, headers=headers)
        page_url = scrapertools.find_single_match(data, patron_new_url)
        page_url = re.sub("\n|\r|\t", "", page_url)

    media_url = scrapertools.find_single_match(data, 'file\s*:\s*"([^"]+)')
    if media_url == '':
        data = scrapertools.find_single_match(data, '(eval\(function.*?)</script>')
        data = jsunpack.unpack(data)
        media_url = scrapertools.find_single_match(data, 'file\s*:\s*"([^"]+)')
    video_urls = [[scrapertools.get_filename_from_url(media_url)[-4:] + " [youwatch]", media_url]]

    for video_url in video_urls:
        logger.info("[youwatch.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = r'//(?:www.)?youwatch.org/(?:embed-)?([A-Za-z0-9]+)(?:-\d+x\d+\.html)?'
    logger.info("youwatch find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for media_id in matches:
        titulo = "[youwatch]"
        url = "http://youwatch.org/embed-%s-640x360.html" % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'youwatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
