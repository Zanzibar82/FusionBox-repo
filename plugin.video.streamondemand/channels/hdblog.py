# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para hdblog
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
#------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "hdblog"
__category__ = "D"
__type__ = "generic"
__title__ = "hdblog (IT)"
__language__ = "IT"


DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.hdblog mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Video recensioni tecnologiche[/COLOR]", action="peliculas", url="http://hardware.hdblog.it/video/", thumbnail="http://www.crat-arct.org/uploads/images/tic%201.jpg"))
    
    return itemlist

def peliculas(item):
    logger.info("streamondemand.hdblog peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron  = '<a class="thumb_new_image" href="([^"]+)">\s*<img[^s]+src="([^"]+)"[^>]+>\s*</a>\s*[^>]+>\s*(.*?)\s*<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", fulltitle=scrapedtitle, show=scrapedtitle, title=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a style=[^f]+f="([^"]+)" class="esteso">Prossima pagina'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="HomePage", title="[COLOR yellow]Torna Home[/COLOR]" , folder=True) )
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR orange]Avanti >>[/COLOR]" , url=scrapedurl , folder=True) )

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

