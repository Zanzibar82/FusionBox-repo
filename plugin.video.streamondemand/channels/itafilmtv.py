# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para itafilmtv
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "itafilmtv"
__category__ = "F,S"
__type__ = "generic"
__title__ = "ITA Film TV"
__language__ = "IT"

host = "http://www.itafilm.tv"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0'],
    ['Accept-Encoding', 'gzip, deflate']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("[itafilmtv.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Novità[/COLOR]",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="genere",
                     title="[COLOR azure]Film Per Genere[/COLOR]",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     action="nazione",
                     title="[COLOR azure]Film Per Nazione[/COLOR]",
                     url=host,
                     thumbnail="http://i.imgur.com/RCkZdTz.png"),
                Item(channel=__channel__,
                     action="anno",
                     title="[COLOR azure]Film Per Anno[/COLOR]",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/Movie%20Year.png"),
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Contenuti Erotici[/COLOR]",
                     url="%s/film-erotici-streaming/" % host,
                     thumbnail="http://orig08.deviantart.net/8008/f/2013/080/9/4/movies_by_musicopath-d5ysmxe.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     action="serietv",
                     title="[COLOR azure]Serie TV[/COLOR]",
                     url="%s/telefilm-serie-tv-streaming/" % host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR orange]Cerca Serie...[/COLOR]",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item, texto):
    logger.info("[itafilmtv.py] " + item.url + " search " + texto)

    item.url = host + "/?do=search&subaction=search&story=" + texto

    try:
        if item.extra == "serie":
            return serietv(item)
        else:
            return fichas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def fichas(item):
    logger.info("[itafilmtv.py] fichas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    action = "findvideos"

    # Extrae las datos
    patron = '<div class="main-news">.*?'
    patron += '<div class="main-news-image"[^<]+'
    patron += '<a href="([^"]+)">'
    patron += '<img src="([^"]+)" '
    patron += 'alt="([^"]+)"'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
                Item(channel=__channel__,
                     action=action,
                     title=scrapedtitle,
                     url=scrapedurl,
                     thumbnail=urlparse.urljoin(host, scrapedthumbnail),
                     fulltitle=scrapedtitle,
                     show=scrapedtitle))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<span>\d+</span> <a href="([^"]+)">')
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR orange]Successivo >>[/COLOR]",
                     url=next_page,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def serietv(item):
    logger.info("[itafilmtv.py] fichas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    action = "episodios"

    # Extrae las datos
    patron = '<div class="main-news">.*?'
    patron += '<div class="main-news-image"[^<]+'
    patron += '<a href="([^"]+)">'
    patron += '<img src="([^"]+)" '
    patron += 'alt="([^"]+)"'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
                Item(channel=__channel__,
                     action=action,
                     title=scrapedtitle,
                     url=scrapedurl,
                     thumbnail=urlparse.urljoin(host, scrapedthumbnail),
                     fulltitle=scrapedtitle,
                     show=scrapedtitle))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<span>\d+</span> <a href="([^"]+)">')
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     action="serietv",
                     title="[COLOR orange]Successivo >>[/COLOR]",
                     url=next_page))

    return itemlist


def genere(item):
    logger.info("[itafilmtv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = '<div class="menu2">(.*?)<div class="left-wrap">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=urlparse.urljoin(host, scrapedurl),
                     folder=True))

    return itemlist


def nazione(item):
    logger.info("[itafilmtv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = '<div class="menu-block-content">(.*?)<div style="clear: both;"></div>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=urlparse.urljoin(host, scrapedurl),
                     folder=True))

    return itemlist


def anno(item):
    logger.info("[itafilmtv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    data = scrapertools.find_single_match(data, '<div class="menu-col fixcol2">(.*?)<div style="clear: both;"></div>')

    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=urlparse.urljoin(host, scrapedurl),
                     folder=True))

    return itemlist


def episodios(item):
    logger.info("[itafilmtv.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    patron = '<div class="main-news-text main-news-text2">(.*?)</div>'
    plot = scrapertools.find_single_match(data, patron)
    plot = scrapertools.htmlclean(plot).strip()

    # Extrae las datos - Episodios
    patron = '<br />(\d+x\d+).*?href="//ads.ad-center.com/[^<]+</a>(.*?)<a href="//ads.ad-center.com/[^<]+</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    if len(matches) == 0:
        patron = ' />(\d+x\d+)(.*?)<br'
        matches = re.compile(patron, re.DOTALL).findall(data)

    # Extrae las datos - sub ITA/ITA
    patron = '<b>.*?STAGIONE.*?(sub|ITA).*?</b>'
    lang = re.compile(patron, re.IGNORECASE).findall(data)

    lang_index = 0
    for scrapedepisode, scrapedurls in matches:

        if int(scrapertools.get_match(scrapedepisode, '\d+x(\d+)')) == 1:
            lang_title = lang[lang_index]
            if lang_title.lower() == "sub": lang_title += " ITA"
            lang_index += 1

        title = scrapedepisode + " (" + lang_title + ")"
        scrapedurls = scrapedurls.replace("playreplay", "moevideo")

        matches_urls = re.compile('href="([^"]+)"', re.DOTALL).findall(scrapedurls)
        urls = ""
        for url in matches_urls:
            urls += url + "|"

        if urls != "":
            itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         title=title, url=urls[:-1],
                         thumbnail=item.thumbnail,
                         plot=plot,
                         fulltitle=item.fulltitle,
                         show=item.show))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
                Item(channel=__channel__,
                     title=item.show,
                     url=item.url,
                     action="add_serie_to_library",
                     extra="episodios",
                     show=item.show))
        itemlist.append(
                Item(channel=item.channel,
                     title="Scarica tutti gli episodi della serie",
                     url=item.url,
                     action="download_all_episodes",
                     extra="episodios",
                     show=item.show))

    return itemlist


def findvideos(item):
    logger.info("[itafilmtv.py] findvideos")

    itemlist = []

    # Extrae las datos
    if "|" not in item.url:
        # Descarga la página
        data = scrapertools.cache_page(item.url, headers=headers)

        sources = scrapertools.get_match(data, '(<noindex> <div class="video-player-plugin">.*?</noindex>)')

        patron = 'src="([^"]+)"'
        matches = re.compile(patron, re.DOTALL).findall(sources)
    else:
        matches = item.url.split('|')

    for scrapedurl in matches:

        server = scrapedurl.split('/')[2].split('.')
        if len(server) == 3:
            server = server[1]
        else:
            server = server[0]

        title = "[COLOR azure]" + item.fulltitle + "[/COLOR]" + " - [" + server + "]"

        itemlist.append(
                Item(channel=__channel__,
                     action="play",
                     title=title,
                     url=scrapedurl,
                     thumbnail=item.thumbnail,
                     fulltitle=item.fulltitle,
                     show=item.show, folder=False))

    return itemlist


def play(item):
    logger.info("[itafilmtv.py] play")

    # Sólo es necesario la url
    data = item.url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.show
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
