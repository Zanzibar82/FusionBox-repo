# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for putstream.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0 + dentaku65
# ------------------------------------------------------------

import re
import time

from core import logger
from core import scrapertools

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate, lzma']
]

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[putstream.py] url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    time.sleep(5)

    post_url = re.findall('Form method="POST" action=\'(.*)\'', data)[0]
    post_selected = re.findall('Form method="POST" action=(.*)</Form>', data, re.DOTALL)[0]

    post_data = 'op=%s&usr_login=%s&id=%s&fname=%s&referer=%s&hash=%s&imhuman=Proceed+to+video' % (
        re.findall('input type="hidden" name="op" value="(.*)"', post_selected)[0],
        re.findall('input type="hidden" name="usr_login" value="(.*)"', post_selected)[0],
        re.findall('input type="hidden" name="id" value="(.*)"', post_selected)[0],
        re.findall('input type="hidden" name="fname" value="(.*)"', post_selected)[0],
        re.findall('input type="hidden" name="referer" value="(.*)"', post_selected)[0],
        re.findall('input type="hidden" name="hash" value="(.*)"', post_selected)[0])

    headers.append(['Referer', page_url])
    data = scrapertools.cache_page(post_url, post=post_data, headers=headers)

    # Extrae la URL
    media_url = scrapertools.get_match( data , 'file:"([^"]+)"' )

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [putstream]",media_url])

    for video_url in video_urls:
        logger.info("[putstream] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = r'//(?:www\.)?putstream\.com/([0-9A-Za-z]+)'
    logger.info("[putstream.py] find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL | re.IGNORECASE).findall(text)

    for media_id in matches:
        titulo = "[putstream]"
        url = 'http://putstream.com/%s' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'putstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
