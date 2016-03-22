# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for abysstream.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------
import re
import urllib

from core import logger
from core import scrapertools

headers = [
    ['Accept-Encoding', 'gzip, deflate'],
    ['User-Agent',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'],
]


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[abysstream.py] url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    stream_link = scrapertools.find_single_match(data, '<input type="hidden" name="streamLink" value="([^"]+)">')
    temp_link = scrapertools.find_single_match(data, '<input type="hidden" name="templink" value="([^"]+)">')

    headers.append(['Referer', page_url])
    post_data = 'streamLink=%s&templink=%s' % (stream_link, temp_link)
    data = scrapertools.cache_page('http://abysstream.com/viewvideo.php', post=post_data, headers=headers)

    # URL
    media_url = scrapertools.find_single_match(data, '<source src="([^"]+)" type="video/mp4"')
    _headers = urllib.urlencode(dict(headers))

    # URL del vídeo
    video_urls.append(
            [scrapertools.get_filename_from_url(media_url)[-4:] + " [Abysstream]", media_url + '|' + _headers])

    for video_url in video_urls:
        logger.info("[abysstream.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://abysstream.net/v/iwbe6genso37
    patronvideos = 'http://abysstream.com/videos/([A-Za-z0-9]+)'
    logger.info("[abysstream.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Abysstream]"
        url = "http://abysstream.com/v/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'abysstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
