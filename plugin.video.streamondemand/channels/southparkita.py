# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para southparkita.altervista.org
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "southparkita"
__category__ = "S,A"
__type__ = "generic"
__title__ = "SouthParkITA Streaming"
__language__ = "IT"

host = "http://southparkita.altervista.org/south-park-ita-streaming/"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("[southparkita.py] mainlist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(host)
    logger.info(data)

    itemlist.append(
        Item(channel=__channel__,
             action="mainlist",
             title="[COLOR green]Ricarica...[/COLOR]"))

    # Extrae las entradas (carpetas)
    patronvideos = '<li id="menu-item-\d{4}.*?\d{4}"><a href="([^"]+)">([^<]+)<\/a><\/li>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)
    for match in matches:
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = match.group(1)
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")

        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=__channel__,
                 action="listepisodes",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl))

    return itemlist


def listepisodes(item):
    logger.info("[southparkita.py] episodeslist")
    logger.info(item.url)
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    cicla = True
    cnt = 2
    while cicla:
        data = data + scrapertools.cache_page(item.url + 'page/' + str(cnt) + '/')
        logger.info(item.url + 'page/' + str(cnt) + '/')
        patronvideos = '<title>Pagina non trovata.*?<\/title>'
        matches = re.compile(patronvideos, re.DOTALL).finditer(data)
        cnt += 1
        logger.info(str(cnt))
        if matches: cicla = False

    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos = '<h1 class="entry-title noMarginTop"><a href="([^"]+)".*?>([^<]+)<\/a><\/h1>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match.group(2)).strip()
        scrapedurl = match.group(1)
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")

        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=item.fulltitle,
                 show=item.show,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title=item.title,
                 url=item.url,
                 action="add_serie_to_library",
                 extra="listepisodes",
                 show=item.show))
        itemlist.append(
            Item(channel=item.channel,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="listepisodes",
                 show=item.show))

    return itemlist
