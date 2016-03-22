# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fastvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
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


def test_video_exists(page_url):
    logger.info("[fastvideo.py] test_video_exists(page_url='%s')" % page_url)

    video_id = scrapertools.find_single_match(page_url, 'me/([A-Za-z0-9]+)')
    url = 'http://www.fastvideo.me/embed-%s-607x360.html' % video_id

    data = scrapertools.cache_page(url, headers=headers)

    if "File was deleted from FastVideo" in data:
        return False, "The file not exists or was removed from FastVideo."

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[fastvideo.py] url=" + page_url)

    video_id = scrapertools.find_single_match(page_url, 'me/([A-Za-z0-9]+)')
    url = 'http://www.fastvideo.me/embed-%s-607x360.html' % video_id

    data = scrapertools.cache_page(url, headers=headers)

    packed = scrapertools.find_single_match(data, "<script type='text/javascript'>eval.function.p,a,c,k,e,.*?</script>")
    unpacked = jsunpack.unpack(packed)
    media_url = scrapertools.find_single_match(unpacked, 'file:"([^"]+)"')

    headers.append(['Referer', page_url])

    _headers = urllib.urlencode(dict(headers))
    # URL del vídeo
    vurl = media_url + '|' + _headers

    video_urls = [[scrapertools.get_filename_from_url(media_url)[-4:] + " [fastvideo.me]", vurl]]

    for video_url in video_urls:
        logger.info("[fastvideo.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    encontrados.add("http://www.fastvideo.me/theme")
    encontrados.add("http://www.fastvideo.me/jquery")
    encontrados.add("http://www.fastvideo.me/s")
    encontrados.add("http://www.fastvideo.me/images")
    encontrados.add("http://www.fastvideo.me/faq")
    encontrados.add("http://www.fastvideo.me/embed")
    encontrados.add("http://www.fastvideo.me/ri")
    encontrados.add("http://www.fastvideo.me/d")
    encontrados.add("http://www.fastvideo.me/css")
    encontrados.add("http://www.fastvideo.me/js")
    encontrados.add("http://www.fastvideo.me/player")
    encontrados.add("http://www.fastvideo.me/cgi")

    # http://www.fastvideo.me/8fw55lppkeps
    patronvideos = 'fastvideo.me/(?:embed-)?([A-Za-z0-9]+)'
    logger.info("[fastvideo.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fastvideo]"
        url = "http://www.fastvideo.me/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fastvideo'])
            encontrados.add(url)
        else:
            logger.info(" url duplicada=" + url)

    return devuelve
