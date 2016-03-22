# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://serietvsubita.net/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "serietvsubita"
__category__ = "S"
__type__ = "generic"
__title__ = "serietvsubita"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://serietvsubita.net"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.channels.serietvsubita mainlist")

    itemlist = [Item(channel=__channel__,
                     action="episodios",
                     title="[COLOR azure]Novità[/COLOR]",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png",
                     folder=True),
                Item(channel=__channel__,
                     action="series",
                     title="[COLOR azure]Indice A-Z[/COLOR]",
                     url=host,
                     thumbnail="http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/A-Z.png",
                     folder=True),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search",
                     folder=True)]
    return itemlist


def search(item, texto):
    logger.info("streamondemand.channels.serietvsubita search")
    item.url = host + "/?s=" + texto + "&op.x=0&op.y=0"

    try:
        return episodios(item)
    # Se captura la excepci?n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def episodios(item):
    logger.info("streamondemand.channels.serietvsubita episodios")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # patron  = '</div><div class="clear"></div>.*?'
    patron = '<h2><a href="([^"]+)".*?title="([^"]+)".*?<p><a href.*?<img.*?src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if scrapedtitle.startswith("Link to "):
            scrapedtitle = scrapedtitle[8:]
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot,
                     folder=True))

    # paginación
    patron = '<div id="navigation">.*?\d+</a> <a href="([^"]+)"'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Post più vecchi...[/COLOR]",
                     url=next_page,
                     action="episodios",
                     extra=item.extra,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def series(item):
    logger.info("streamondemand.channels.serietvsubita series")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<li id="widget_categories" class="widget png_scale"><h2 class="blocktitle"><span>Serie</span>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li class="cat-item[^<]+<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        thumbnail = ""
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url, scrapedurl)

        if (DEBUG): logger.info("title=[" + title + "], url=[" + url + "], thumbnail=[" + thumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="episodiosearch",
                     title="[COLOR azure]" + title + "[/COLOR]",
                     url=url,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png",
                     folder=True))

    # paginación
    patron = '<div id="navigation">.*?\d+</a> <a href="([^"]+)"'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Episodi precedenti...[/COLOR]",
                     url=next_page,
                     action="series",
                     extra=item.extra,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def episodiosearch(item):
    logger.info("streamondemand.channels.serietvsubita episodios")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<div class="post-meta">.*?<a href="([^"]+)" title="([^"]+)".*?<img.*?src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot,
                     folder=True))

    # paginación
    patron = '<div id="navigation">.*?\d+</a> <a href="([^"]+)"'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Episodi precedenti...[/COLOR]",
                     url=next_page,
                     action="episodios",
                     extra=item.extra,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist
