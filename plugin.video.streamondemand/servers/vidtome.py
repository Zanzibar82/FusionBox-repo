# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidto.me
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import jsunpack
from core import logger
from core import scrapertools

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate']
]


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("streamondemand.servers.vidtome url=" + page_url)

    data = scrapertools.cache_page(page_url, headers=headers)
    # logger.info("data="+data)

    op = scrapertools.get_match(data, '<input type="hidden" name="op" value="([^"]+)"')
    usr_login = ""
    id = scrapertools.get_match(data, '<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(data, '<input type="hidden" name="fname" value="([^"]+)"')
    referer = scrapertools.get_match(data, '<input type="hidden" name="referer" value="([^"]*)"')
    hashstring = scrapertools.get_match(data, '<input type="hidden" name="hash" value="([^"]*)"')
    imhuman = scrapertools.get_match(data, '<input type="submit".*?name="imhuman" value="([^"]+)"').replace(" ", "+")

    import time
    time.sleep(10)

    post = "op=" + op + "&usr_login=" + usr_login + "&id=" + id + "&fname=" + fname + "&referer=" + referer + "&hash=" + hashstring + "&imhuman=" + imhuman
    headers.append(["Referer", page_url])
    body = scrapertools.cache_page(page_url, post=post, headers=headers)

    patron = "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>"
    data = scrapertools.find_single_match(body, patron)
    data = jsunpack.unpack(data)

    media_urls = re.findall(r'\{label:"([^"]+)",file:"([^"]+)"\}', data)
    video_urls = []
    for label, media_url in media_urls:
        video_urls.append(
            [scrapertools.get_filename_from_url(media_url)[-4:] + " (" + label + ") [vidto.me]", media_url])

    patron = '<a id="lnk_download" href="([^"]+)"'
    media_url = scrapertools.find_single_match(body, patron)
    if media_url != "":
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (ORIGINAL) [vidto.me]", media_url])

    for video_url in video_urls:
        logger.info("streamondemand.servers.vidtome %s - %s" % (video_url[0], video_url[1]))

    return video_urls


def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = r'//(?:www\.)?vidto\.me/(?:embed-)?([0-9A-Za-z]+)'
    logger.info("streamondemand.servers.vidtome find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidto.me]"
        url = "http://vidto.me/" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidtome'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
