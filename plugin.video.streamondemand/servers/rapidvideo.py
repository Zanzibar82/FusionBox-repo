# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urllib

from core import jsunpack
from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[rapidvideo.py] url=" + page_url)
    video_urls = []

    headers = [
        ['User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'],
        ['Accept-Encoding', 'gzip, deflate'],
        ['Referer', page_url]
    ]

    data = scrapertools.cache_page(page_url)

    op = scrapertools.find_single_match(data, 'name="op" value="([^"]+)"')
    usr_login = scrapertools.find_single_match(data, 'name="usr_login" value="([^"]+)"')
    id = scrapertools.find_single_match(data, 'name="id" value="([^"]+)"')
    fname = scrapertools.find_single_match(data, 'name="fname" value="([^"]+)"')
    referer = scrapertools.find_single_match(data, 'name="referer" value="([^"]+)"')
    hash = scrapertools.find_single_match(data, 'name="hash" value="([^"]+)"')
    imhuman = scrapertools.find_single_match(data, 'name="imhuman" value="([^"]+)"')

    post = "op=%s&usr_login=%s&id=%s&fname=%s&referer=%s&hash=%s&imhuman=%s" % (op, usr_login, id, fname, referer, hash, imhuman)

    data = scrapertools.cache_page(page_url, post=post, headers=headers)

    packed = scrapertools.get_match(data, "<script type='text/javascript'>eval.function.p,a,c,k,e,.*?</script>")
    unpacked = jsunpack.unpack(packed)
    media_url = scrapertools.find_single_match(unpacked, 'file:"([^"]+)"')

    video_urls.append(["[rapidvideo]", media_url + '|' + urllib.urlencode(dict(headers))])

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.rapidvideo.org/ttsvqng2qp2v/Scooby-Doo_e_la_Maschera_di_Blue_Falcon_720p.mp4.html
    patronvideos = 'rapidvideo.org/([A-Za-z0-9]+)/'
    logger.info("[rapidvideo.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.org/" + match
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d, '"fname" value="([^<]+)"')
        ma = titulo + " " + ma
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([ma, url, 'rapidvideo'])

            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve


def test():
    video_urls = get_video_url("http://www.rapidvideo.com/embed/sy6wen17")

    return len(video_urls) > 0
