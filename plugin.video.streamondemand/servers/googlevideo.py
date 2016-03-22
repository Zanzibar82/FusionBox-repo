# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Google Video
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
# modify by DrZ3r0

import re

from core import logger

fmt_value = {
    5: "240p h263 flv",
    18: "360p h264 mp4",
    22: "720p h264 mp4",
    26: "???",
    33: "???",
    34: "360p h264 flv",
    35: "480p h264 flv",
    37: "1080p h264 mp4",
    36: "3gpp",
    38: "720p vp8 webm",
    43: "360p h264 flv",
    44: "480p vp8 webm",
    45: "720p vp8 webm",
    46: "520p vp8 webm",
    59: "480 for rtmpe",
    78: "400 for rtmpe",
    82: "360p h264 stereo",
    83: "240p h264 stereo",
    84: "720p h264 stereo",
    85: "520p h264 stereo",
    100: "360p vp8 webm stereo",
    101: "480p vp8 webm stereo",
    102: "720p vp8 webm stereo",
    120: "hd720",
    121: "hd1080"
}


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[googlevideo.py] get_video_url(page_url='%s')" % page_url)

    video_urls = [["[googlevideo]", page_url]]

    for video_url in video_urls:
        logger.info("[googlevideo.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra v�deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = r"""(https?://(?:redirector\.)?googlevideo.com/[^"']+)(?:",\s*"label":\s*([0-9]+),)?"""
    logger.info("[googlevideo.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        titulo = "[googlevideo]" if match.group(2) is None else "[googlevideo %s]" % match.group(2)
        url = match.group(1)

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'googlevideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = r'(https?://(?:lh.\.)?googleusercontent.com/[^=]+=m(\d+))'
    logger.info("[googlevideo.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        titulo = "[googlevideo]" if match.group(2) is None else "[googlevideo %s]" % fmt_value[int(match.group(2))]
        url = match.group(1)

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'googlevideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
