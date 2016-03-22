# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para hdstreamingit
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import base64
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "hdstreamingit"
__category__ = "F"
__type__ = "generic"
__title__ = "hd-streaming.it (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.hd-streaming.it"

key = base64.urlsafe_b64decode(
        'ZTViNTA5OGJhMWU1NDNlNGFiMGNjNThiNWYzYjE5NTg4MzE3YmQ3NjczMjliZGNiODk0ZDg5YjU2MGU1NTJjMDY4ZjFmOWI5NTc5Zjc0NjQ4MmU2YzEyNGViNzQzYmFlY2MyZmVkZTIyNDk5YzA2NGNiMjZjYTQ1ZDlmM2Y1ODFkMmRjZWM4YjdmNmY0ZmI5YmJhMTgyZmQ4Nzc2NzQyYg==')

importio_url = "https://api.import.io/store/connector/_magic?format=JSON&js=false&_apikey=%s&url=" % key


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.hdstreamingit mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url="%s/event_categories/film/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film 3D[/COLOR]",
                     action="pelis3d",
                     url="%s/event_categories/film-3d/" % host,
                     thumbnail="http://i.imgur.com/wXMmQie.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="peliculas",
                     extra="serie",
                     url="%s/event_categories/serie-tv/" % host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def search(item, texto):
    logger.info("[hdstreamingit.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto + "&search=Cerca"
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.get_match(data, '<ul class="sub-menu">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=urlparse.urljoin(host, scrapedurl),
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png",
                     folder=True))

    return itemlist


def peliculas(item):
    logger.info("streamondemand.hdstreamingit peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, timeout=5)

    # Extrae las entradas (carpetas)
    patronvideos = '<a class="link_image" href="[^"]+" title="Permalink to (.*?)">.*?'
    patronvideos += '<img src="([^"]+)" alt="">.*?'
    patronvideos += '<div class="button_yellow"><a(?: target="_blank")? href="([^"]+)"'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url, match.group(3))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedtitle = scrapertools.unescape(match.group(1))
        scrapedplot = ""
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action='episodios' if item.extra == 'serie' else 'findvideos',
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl if item.extra == 'serie' else importio_url + scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot,
                     folder=True))

    # Extrae el paginador
    patronvideos = "<link rel='next' href='([^']+)' />"
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

def pelis3d(item):
    logger.info("streamondemand.hdstreamingit peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = r'<div class="button_red"><a href="([^"]+)"[^>]+>[^>]+>[^>]+>\s*<div class="button_yellow">[^>]+>Versione 3D</a><input type="hidden" value="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedplot = ""
        # html = scrapertools.cache_page(scrapedtitle)
        # start = html.find("<h1>TRAMA</h1>")
        # end = html.find("</p>", start)
        # scrapedplot = html[start:end]
        # scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        # scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapedtitle.replace("http://www.hd-streaming.it/movies/", " ")
        scrapedtitle = scrapedtitle.replace("/", " ")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("-", " "))
        scrapedtitle = ' '.join(word[0].upper() + word[1:] for word in scrapedtitle.split())
        scrapedthumbnail = ""
        if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action='episodios' if item.extra == 'serie' else 'findvideos',
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl if item.extra == 'serie' else importio_url + scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot,
                     folder=True))

    # Extrae el paginador
    patronvideos = "<link rel='next' href='([^']+)' />"
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
                 action="pelis3d",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

def episodios(item):
    logger.info("streamondemand.hdstreamingit episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    start = data.find('id="stagioni"')
    end = data.find('id="disqus_thread"', start)

    data = data[start:end]

    patron = '(.*?)<a href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patron).findall(data)
    for title1, url, title2 in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(title1 + title2)
        scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
        itemlist.append(
                Item(channel=__channel__,
                     action='findvideos',
                     fulltitle=item.fulltitle,
                     show=item.show,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=importio_url + url,
                     thumbnail=item.thumbnail,
                     plot=item.plot,
                     folder=True))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
                Item(channel=__channel__,
                     title=item.title,
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
