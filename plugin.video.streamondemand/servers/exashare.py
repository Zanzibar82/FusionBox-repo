# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for exashare.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate, lzma']]


def test_video_exists(page_url):
    logger.info("[exashare.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url, headers=headers)

    if re.search("""File Not Found""", data):
        return False, 'File Not Found or Removed.'

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[exashare.py] url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    try:
        page_url = re.search('src="([^"]+)', data).group(1)
    except:
        return video_urls

    data = scrapertools.cache_page(page_url, headers=headers)

    # URL del vídeo
    url = re.search('file\s*:\s*"(http.+?)"', data)
    if url:
        url = url.group(1)
        video_urls.append([scrapertools.get_filename_from_url(url)[-4:] + " [exashare]", url])

    return video_urls  # Encuentra vídeos del servidor en el texto pasado


def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = r'//(?:www\.)?exashare\.com/(?:embed-)?(?!make)(?!image)(?!login)(?!contact)(?!player)([0-9A-Za-z]+)(?:\-[0-9]+x[0-9]+\.html)?'
    logger.info("[exashare.py] find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for media_id in matches:
        titulo = "[exashare]"
        url = 'http://exashare.com/embed-%s.html' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'exashare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
