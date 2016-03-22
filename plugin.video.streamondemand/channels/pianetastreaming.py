# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "pianetastreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "pianetastreaming.net (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.pianetastreaming.net"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.pianetastreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Scegli Per Genere[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Scegli Per Anno[/COLOR]",
                     action="catbyyear",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/Movie%20Year.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]
    return itemlist


def peliculas(item):
    logger.info("streamondemand.pianetastreaming peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="moviefilm">.*?<a href="([^"]+)">.*?<img src="([^"]+)" alt="([^"]+)" height.*?/></a>.*?<div class="movief">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        #html = scrapertools.cache_page(scrapedurl)
        #start = html.find("<h2>")
        #end = html.find("</iframe></p>", start)
        #scrapedplot = html[start:end]
        #scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        #scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        if (DEBUG): logger.info(
                "url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "], title=[" + scrapedtitle + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     folder=True,
                     fanart=scrapedthumbnail,
                     plot=scrapedplot))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

def categorias(item):
    logger.info("streamondemand.pianetastreaming categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # Narrow search by selecting only the combo
    patron = '<ul class="sub-menu">(.*?)</ul>'
    bloque = scrapertools.find_single_match(data, patron)

    # The categories are the options for the combo  
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot))

    return itemlist


def catbyyear(item):
    logger.info("streamondemand.pianetastreaming categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # Narrow search by selecting only the combo
    patron = '<li id="menu-item-9242" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-9242"><a>Scegli Per Anno</a>(.*?)</ul>'
    bloque = scrapertools.find_single_match(data, patron)

    # The categories are the options for the combo  
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[pianetastreaming.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
