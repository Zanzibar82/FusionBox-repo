# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para mondolunatico
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import os
import re
import sys
import urllib
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mondolunatico"
__category__ = "F"
__type__ = "generic"
__title__ = "Mondo Lunatico"
__language__ = "IT"

host = "http://mondolunatico.org"

captcha_url = '%s/pass/CaptchaSecurityImages.php?width=100&height=40&characters=5' % host

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Connection', 'keep-alive']
]

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.mondolunatico mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Novità[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist

def categorias(item):
    logger.info("streamondemand.mondolunatico categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<option class="level-0" value="7">(.*?)<option class="level-0" value="8">')

    # The categories are the options for the combo
    patron = '<option class=[^=]+="([^"]+)">(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("&nbsp;",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("(",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace(")",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("0",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("1",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("2",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("3",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("4",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("5",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("6",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("7",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("8",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("9",""))
        scrapedurl= "http://mondolunatico.org/category/film-per-genere/"+scrapedtitle
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
    logger.info("[mondolunatico.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.mondolunatico peliculas")

    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="boxentry">\s*<a href="([^"]+)"[^>]+>\s*<img src="([^"]+)" alt="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, in matches:
        scrapedplot = ""
        #html = scrapertools.cache_page(scrapedurl)
        #start = html.find("Trama del ")
        #end = html.find("<div id=\"wrpbody\" class=\"wrphidden\"></div>", start)
        #scrapedplot = html[start:end]
        #scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        #scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        title = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 viewmode="movie_with_plot"))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">'
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

def findvideos(item):
    logger.info("streamondemand.mondolunatico findvideos")

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    # Extrae las entradas
    patron = r'noshade>(.*?)<br>.*?<a href="(http://mondolunatico\.org/pass/index\.php\?ID=[^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapedtitle.replace('*', '').replace('Streaming', '').strip()
        title = '%s - [%s]' % (item.title, scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 fulltitle=item.fulltitle,
                 show=item.show,
                 server='captcha',
                 folder=False))

    return itemlist


def play(item):
    logger.info("streamondemand.mondolunatico play")

    itemlist = []

    if item.server == 'captcha':
        headers.append(['Referer', item.url])

        # Descarga la página
        data = scrapertools.cache_page(item.url, headers=headers)

        if 'CaptchaSecurityImages.php' in data:
            # Descarga el captcha
            img_content = scrapertools.cache_page(captcha_url, headers=headers)

            captcha_fname = os.path.join(config.get_data_path(), __channel__ + "captcha.img")
            with open(captcha_fname, 'wb') as ff:
                ff.write(img_content)

            from platformcode import captcha

            keyb = captcha.Keyboard(heading='', captcha=captcha_fname)
            keyb.doModal()
            if keyb.isConfirmed():
                captcha_text = keyb.getText()
                post_data = urllib.urlencode({'submit1': 'Invia', 'security_code': captcha_text})
                data = scrapertools.cache_page(item.url, post=post_data, headers=headers)

            try:
                os.remove(captcha_fname)
            except:
                pass

        itemlist.extend(servertools.find_video_items(data=data))

        for videoitem in itemlist:
            videoitem.title = item.title
            videoitem.fulltitle = item.fulltitle
            videoitem.thumbnail = item.thumbnail
            videoitem.show = item.show
            videoitem.plot = item.plot
            videoitem.channel = __channel__
    else:
        itemlist.append(item)

    return itemlist
