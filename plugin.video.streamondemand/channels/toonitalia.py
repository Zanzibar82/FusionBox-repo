# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per toointalia
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import urlparse
import re
import sys

from core import scrapertools
from core import logger
from core import config
from core.item import Item
from servers import servertools
from servers import adfly

__channel__ = "toonitalia"
__category__ = "A"
__type__ = "generic"
__title__ = "Toonitalia"
__language__ = "IT"

host = "http://toonitalia.altervista.org/"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.toointalia mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Home[/COLOR]", action="anime", url=host, thumbnail="http://i.imgur.com/a8Vwz1V.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Anime[/COLOR]" , action="anime", url=host+"/category/anime/",thumbnail="http://i.imgur.com/a8Vwz1V.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Anime Sub-Ita[/COLOR]", action="anime", url=host+"/category/anime-sub-ita/", thumbnail="http://i.imgur.com/a8Vwz1V.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Film Animazione[/COLOR]", action="animazione", url=host+"/category/film-animazione/", thumbnail="http://i.imgur.com/a8Vwz1V.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Serie TV[/COLOR]", action="anime", url=host+"/category/serie-tv/", thumbnail="http://i.imgur.com/a8Vwz1V.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Cerca...[/COLOR]", action="search", thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"))

    return itemlist

def search(item,texto):
    logger.info("[toonitalia.py] "+item.url+" search "+texto)
    item.url = "http://toonitalia.altervista.org/?s="+texto
    try:
        return anime(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []	


def anime( item ):
    logger.info( "streamondemand.toointalia peliculas" )

    itemlist = []

    ## Descarga la pagina
    data = scrapertools.cache_page(item.url)

    ## Extrae las entradas (carpetas)
    patron  = '<figure class="post-image left">.*?<a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)" /></a>'
    matches = re.compile( patron, re.DOTALL ).findall( data )

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.decodeHtmlentities( scrapedtitle )
 
        itemlist.append( Item( channel=__channel__, action="episodi", title=title, url=scrapedurl, thumbnail=scrapedthumbnail, fulltitle=title, show=title , viewmode="movie_with_plot") )

    # Older Entries
    patron = '<link rel="next" href="([^"]+)" />'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Post più vecchi...[/COLOR]",
                     url=next_page,
                     action="anime",
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))
					 
    return itemlist	

def animazione( item ):
    logger.info( "streamondemand.toointalia peliculas" )

    itemlist = []

    ## Descarga la pagina
    data = scrapertools.cache_page( item.url )

    ## Extrae las entradas (carpetas)
    patron  = '<figure class="post-image left">.*?<a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)" /></a>'
    matches = re.compile( patron, re.DOTALL ).findall( data )

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.decodeHtmlentities( scrapedtitle )
 
        itemlist.append( Item( channel=__channel__, action="film", title=title, url=scrapedurl, thumbnail=scrapedthumbnail, fulltitle=title, show=title , viewmode="movie_with_plot") )
    # Older Entries
    patron = '<link rel="next" href="([^"]+)" />'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Post più vecchi...[/COLOR]",
                     url=next_page,
                     action="animazione",
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))
					 
    return itemlist	
	
def episodi(item):
    logger.info("toonitalia.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url)
    # Extracts the entries
    patron = '<a.*?href="([^"]+)".*?target="_blank">([^"]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     thumbnail=item.thumbnail,
                     url=scrapedurl))

    return itemlist

def film(item):
    logger.info("toonitalia.py film")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url)
    # Extracts the entries
#    patron = '<img class="aligncenter.*?src="([^"]+)" alt="([^"]+)".*?<strong><a href="([^"]+)" target="_blank">'
    patron = '<img.*?src="([^"]+)".*?alt="([^"]+)".*?strong><a href="([^"]+)" target="_blank">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail,scrapedtitle,scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     thumbnail=scrapedthumbnail,
                     url=scrapedurl))
    # Older Entries
    patron = '<link rel="next" href="([^"]+)" />'
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR orange]Post più vecchi...[/COLOR]",
                     url=next_page,
                     action="film",
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))
    return itemlist	
	
def findvid(item):
    logger.info("[toonitalia.py] findvideos")
    #Avoids flashx 503 error on winOS
    import time
    time.sleep(10)

    # Downloads page
    data = item.url
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
