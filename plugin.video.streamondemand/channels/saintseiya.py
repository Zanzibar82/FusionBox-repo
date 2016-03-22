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

__channel__ = "saintseiya"
__category__ = "A"
__type__ = "generic"
__title__ = "Saint Seiya"
__language__ = "IT"

DEBUG = config.get_setting("debug")

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate']
]

host = "http://archive.forumcommunity.net"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[saintseiya.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Saint Seiya - Saga I - VIII[/COLOR]",
                     action="episodi",
                     url="%s/?t=47797121" % host,
                     thumbnail="http://www.sentieriselvaggi.it/wp-content/uploads/public/articoli/14593/Images/200604250765114593.jpg",
                     fanart="http://wfiles.brothersoft.com/s/saint-seiya-wallpaper_153109-1280x720.jpg"),
                Item(channel=__channel__,
                     title="[COLOR azure]Saint Seiya - Hades[/COLOR]",
                     action="episodihades",
                     url="%s/?t=39222201" % host,
                     thumbnail="http://imagenes.asia-team.net/afiche/1800.jpg",
                     fanart="http://cartoonsimages.com/sites/default/files/field/image/Saint_Seiya_Hades_Elysion_by_Juni_Anker.jpg"),
                Item(channel=__channel__,
                     title="[COLOR azure]Saint Seiya - Soul Of Gold[/COLOR]",
                     action="episodisoul",
                     url="http://pastebin.com/XsdtYBhU",
                     thumbnail="http://i.imgur.com/0rYG1mV.jpg",
                     fanart="http://vignette4.wikia.nocookie.net/saintseiya/images/8/8e/Gold_Saints_%28No_Cloths%29.png/revision/latest?cb=20150413225923"),
                Item(channel=__channel__,
                     title="[COLOR azure]Saint Seiya - Omega[/COLOR]",
                     action="episodiomega",
                     url="%s/?t=50446785" % host,
                     thumbnail="http://41.media.tumblr.com/646ae07c78acbb7dd0b32dca6febc2b3/tumblr_mo1n061YrE1rvobogo1_500.jpg",
                     fanart="http://cartoonsimages.com/sites/default/files/field/image/Saint%2BSeiya%2BOmega.jpg"),
                Item(channel=__channel__,
                     title="[COLOR azure]Saint Seiya - The Lost Canvas[/COLOR]",
                     action="episodicanvas",
                     url="%s/?t=53018304" % host,
                     thumbnail="https://www.topanimestream.com/ImageHost/53/33/Saint_Seiya_The_Lost_Canvas__Meiou_Shinwa_2_poster.jpg",
                     fanart="http://i.ytimg.com/vi/9QQX6Rtw1IU/maxresdefault.jpg")]

    return itemlist


def episodi(item):
    logger.info("saintseiya.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extracts the entries
    patron = "Saga della Guerra Galattica</span></b><br>(.*?)<br></p><br><br><span class="
    bloque = scrapertools.find_single_match(data, patron)

    patron = '<br>(.*?)<a href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for tit1, scrapedurl, tit2 in matches:
        scrapedtitle = tit1 + tit2
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("<b>", ""))
        scrapedtitle = scrapertools.htmlclean(scrapedtitle).strip()
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     url=scrapedurl,
                     fanart="http://wfiles.brothersoft.com/s/saint-seiya-wallpaper_153109-1280x720.jpg",
                     thumbnail="http://www.toei-animation.com/files/visuels/Saint_Seiya.jpg"))

    return itemlist


def episodihades(item):
    logger.info("saintseiya.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extracts the entries
    patron = "<b>SANTUARIO:</b></span><br>(.*?)<br></p><br><br><span class="
    bloque = scrapertools.find_single_match(data, patron)

    patron = '<a href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     url=scrapedurl,
                     fanart="http://wfiles.brothersoft.com/s/saint-seiya-wallpaper_153109-1280x720.jpg",
                     thumbnail="http://www.animeemanga.it/wp-content/uploads/2012/02/I-Cavalieri-dello-Zodicao-Hades-Chapter-Inferno-Pegasus-Sirio-Crystal-Andromeda-Phoenix-Hades-Pandora-Radamantis-Minosse-Eaco.jpg"))

    return itemlist


def episodiomega(item):
    logger.info("saintseiya.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extracts the entries
    patron = "<i>Episodi Saint Seya Omega Streming </i></span></b></span><br><br>(.*?)<br><br><br><br><br>Si Ringrazia"
    bloque = scrapertools.find_single_match(data, patron)

    patron = '<br>(.*?)<a href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for tit1, scrapedurl, tit2 in matches:
        scrapedtitle = tit1 + tit2
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     url=scrapedurl,
                     fanart="http://wfiles.brothersoft.com/s/saint-seiya-wallpaper_153109-1280x720.jpg",
                     thumbnail="http://www.toei-animation.com/files/visuels/Saint_Seiya.jpg"))

    return itemlist


def episodicanvas(item):
    logger.info("saintseiya.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extracts the entries
    patron = ">Saint Seiya: The Lost Canvas Sub Ita Streaming</span></b></i></span><br>(.*?)Saint Seiya: The Lost Canvas Sub Ita Download"
    bloque = scrapertools.find_single_match(data, patron)

    patron = '<br>(.*?)<a href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for tit1, scrapedurl, tit2 in matches:
        scrapedtitle = tit1 + tit2
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     url=scrapedurl,
                     fanart="http://wfiles.brothersoft.com/s/saint-seiya-wallpaper_153109-1280x720.jpg",
                     thumbnail="http://media.comicsblog.it/N/New/News5890.jpg"))

    return itemlist


def episodisoul(item):
    logger.info("saintseiya.py episodi")

    itemlist = []

    # Downloads page
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extracts the entries
    patron = '>&lt;br&gt;(.*?)&lt;a href=&quot;(.*?)&quot; target=&quot;_blank&quot;&gt;'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
                Item(channel=__channel__,
                     action="findvid",
                     title=scrapedtitle,
                     url=scrapedurl,
                     fanart="http://ib3.huluim.com/show/22747?size=476x268&region=US",
                     thumbnail="http://4.bp.blogspot.com/-3o0SH8YNW3k/VXNxuNfiXxI/AAAAAAAABYk/tjuOx7DdlxI/s1600/%255BHorribleSubs%255D%2BSaint%2BSeiya%2B-%2BSoul%2Bof%2BGold%2B-%2B05%2B%255B720p%255D.mkv_snapshot_17.26_%255B2015.06.06_23.09.44%255D.jpg"))

    return itemlist


def findvid(item):
    logger.info("[saintseiya.py] findvideos")

    # Downloads page
    data = item.url

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
