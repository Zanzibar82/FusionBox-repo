# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canale pastebin
# http://www.mimediacenter.info/foro/viewforum.php?f=36
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

__channel__ = "pastebin"
__category__ = "F,A,S,VOS"
__type__ = "generic"
__title__ = "Pastebin"
__language__ = ""

DEBUG = config.get_setting("debug")

def isGeneric():
    return True
'''
1) Sintassi per caricare lista film su pastebin.com (esempio su http://pastebin.com/XsdtYBhU) :

<br>TITOLO FILM 1<a href="LINK URL AL VIDEO TRA QUESTE VIRGOLETTE http://etc etc" target="_blank">
<br>TITOLO FILM 2<a href="LINK URL AL VIDEO TRA QUESTE VIRGOLETTE http://etc etc" target="_blank">
<br>TITOLO FILM ETC...<a href="LINK URL AL VIDEO TRA QUESTE VIRGOLETTE http://etc etc" target="_blank">

2) Salvare il file su pastebin.com selezionando "Expires: NEVER"

3) Inserire il codice nel canale pastebin per accedere alla lista (es.: http://pastebin.com/XsdtYBhU = codice da inserire: XsdtYBhU )

'''
def mainlist(item):
    logger.info("[pastebin.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search", title="Inserisci codice pagina pastebin.com"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[pastebin.py] search texto="+texto)

    item.url = "http://pastebin.com/"+texto
    return ricercautente(item)

def ricercautente(item):
    logger.info("pastebin.py ricercautente")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url)
    # Extracts the entries
    patron = '>&lt;br&gt;(.*?)&lt;a href=&quot;(.*?)&quot; target=&quot;_blank&quot;&gt;'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="findvid",
                 title=scrapedtitle,
                 url=scrapedurl))

    return itemlist

def findvid(item):
    logger.info("[pastebin.py] findvideos")

    # Downloads page
    data = item.url

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
