# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para tenentecolombo
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import urlparse
import re
import sys

from core import scrapertools
from core import logger
from core import config
from core.item import Item
from servers import servertools

__channel__ = "tenentecolombo"
__category__ = "S"
__type__ = "generic"
__title__ = "Tenente Colombo Streaming"
__language__ = "IT"

host = "http://mondolunatico.altervista.org/blog/il-tenente-colombo-serie-tv/"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.tenentecolombo mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Tenente Colombo - Tutti gli episodi[/COLOR]", action="peliculas", url="http://mondolunatico.altervista.org/blog/il-tenente-colombo-serie-tv/", thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"))
    
    return itemlist


def peliculas( item ):
    logger.info( "streamondemand.tenentecolombo peliculas" )

    itemlist = []

    ## Descarga la pagina
    data = scrapertools.cache_page( item.url )

    ## Extrae las entradas (carpetas)
    patron  = '<br>\s*<a href="([^"]+)"[^>]+>(.*?)</a>[^_]+_[^>]+>Openload<'
    #patron  = '<a href="http://put[^>]+>(.*?)</a>.*?.htm.(.*?)"[^>]+>Openload</a>'
    matches = re.compile( patron, re.DOTALL ).findall( data )

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        title = scrapertools.decodeHtmlentities( scrapedtitle )
 
        itemlist.append( Item( channel=__channel__, action="play", title=title, url=scrapedurl, thumbnail=scrapedthumbnail, fulltitle=title, show=title , plot=scrapedplot , viewmode="movie_with_plot") )

    return itemlist

def play(item):
    logger.info("[tenentecolombo.py] play")

    ## Sólo es necesario la url
    data = item.url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.show
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
