# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for akstream.net
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------

import re
import urllib

from core import logger
from core import scrapertools
from lib import mechanize

headers = [
    ['User-Agent',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'],
]


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[akstream.py] url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    vid = scrapertools.find_single_match(data, '<input type="hidden" name="streamLink" value="([^"]+)">')

    headers.append(['Referer', page_url])
    post_data = 'streamLink=%s' % vid
    data = scrapertools.cache_page('http://akstream.video/viewvideo.php', post=post_data, headers=headers)

    # URL
    media_url = scrapertools.find_single_match(data, '<source src="([^"]+)" type="video/mp4"')
    _headers = urllib.urlencode(dict(headers))

    # URL del vídeo
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [Akstream]", media_url + '|' + _headers])

    for video_url in video_urls:
        logger.info("[akstream.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://akstream.net/v/iwbe6genso37
    patronvideos = 'http://akstream.(?:net|video)/(?:v|videos)/([a-z0-9]+)'
    logger.info("[akstream.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Akstream]"
        url = "http://akstream.video/stream/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'akstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://vcrypt.net/sak/0a8hqibleus5
    # Filmpertutti.eu
    br = mechanize.Browser()
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0')]
    br.set_handle_robots(False)
    br.set_handle_gzip(True)
    patronvideos = 'http://vcrypt.net/sak/([^"]+)'
    matches = re.compile(patronvideos, re.DOTALL).findall(text)
    page = scrapertools.find_single_match(text, 'rel="canonical" href="([^"]+)"')

    for match in matches:
        titulo = "[Akstream]"
        url = "http://vcrypt.net/sak/" + match
        r = br.open(url)
        data = r.read()
        vid = scrapertools.find_single_match(data, 'akstream.(?:net|video)/(?:v|videos)/([^"]+)"')
        url = "http://akstream.video/stream/" + vid
        if url not in encontrados and vid != "":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'akstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve


def test():
    video_urls = get_video_url("http://akstream.net/v/8513acv2alss")

    return len(video_urls) > 0
