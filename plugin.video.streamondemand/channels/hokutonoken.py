# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per I Cavalieri Dello Zodiaco
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "hokutonoken"
__category__ = "A"
__type__ = "generic"
__title__ = "Hokuto no Ken"
__language__ = "IT"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("[hokutonoken.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Hokuto no Ken - Prima Serie[/COLOR]",
                     action="episodi",
                     url="http://pastebin.com/BUqD13hb",
                     thumbnail="http://i.imgur.com/MGkqu7c.jpg",
                     fanart="http://fullhdwp.com/images/wallpapers/Group-fist-of-the-north-star-wallpaper-.jpg"),
                Item(channel=__channel__,
                     title="[COLOR azure]Hokuto no Ken - Seconda Serie[/COLOR]",
                     action="episodi",
                     url="http://pastebin.com/mHXQRBxZ",
                     thumbnail="http://i159.photobucket.com/albums/t123/Janthem/hnk2.jpg",
                     fanart="http://fullhdwp.com/images/wallpapers/Group-fist-of-the-north-star-wallpaper-.jpg")]

    return itemlist


def episodi(item):
    logger.info("hokutonoken.py episodi")

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
                     thumbnail=item.thumbnail,
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
