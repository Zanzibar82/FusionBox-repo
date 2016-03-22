# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Sito hdgratis.net  by SchisM
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import urllib2

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "hdgratis"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "HDGratis"
__language__ = "IT"

host = "http://hdgratis.net"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("[hdgratis.py] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Al Cinema[/COLOR]",
             action="fichas",
             url=host + "/in-sala/",
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),

        Item(channel=__channel__,
             title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
             action="fichas",
             url=host + "/nuove-uscite/",
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),

        Item(channel=__channel__,
             title="[COLOR azure]Film Sub-Ita[/COLOR]",
             action="fichas",
             url=host + "/sub-ita/",
             thumbnail="http://i.imgur.com/qUENzxl.png"),			 
			 

        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def search(item, texto):
    logger.info("[hdgratis.py] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return getsearch(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def genere(item):
    logger.info("[hdgratis.py] genere")
    itemlist = []

    data = anti_cloudflare(item.url)

    patron = '<a href="http://hdgratis.net/film/">Film</a>(.+?)</ul>'
    data = scrapertools.find_single_match(data, patron)
    
    patron = '<li class=".*?'
    patron += 'href="([^"]+)".*?'
    patron += '>([^"]+)</a>'
    
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace('&amp;','-')
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title=scrapedtitle,
                     url=scrapedurl,
                     folder=True))

    return itemlist


def getsearch(item):
    logger.info("[hdgratis.py] fichas")

    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare(item.url)
    # fix - calidad

    # ------------------------------------------------
    cookies = ""
    matches = re.compile('(.italiafilm.video.*?)\n', re.DOTALL).findall(config.get_cookie_data())
    for cookie in matches:
        name = cookie.split('\t')[5]
        value = cookie.split('\t')[6]
        cookies += name + "=" + value + ";"
    headers.append(['Cookie', cookies[:-1]])
    import urllib
    _headers = urllib.urlencode(dict(headers))
    # ------------------------------------------------

    patron = '<div class="col-xs-2">.*?'
    patron += 'href="([^"]+)".*?'
    patron += 'title="([^"]+)".*?'
    patron += '<img src="([^"]+)".*?'
       

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scraped_2, scrapedtitle, scrapedthumbnail in matches:

        scrapedurl = scraped_2
        


        title = scrapertools.decodeHtmlentities(scrapedtitle)
        # title += " (" + scrapedcalidad + ")

        # ------------------------------------------------
        scrapedthumbnail += "|" + _headers
        # ------------------------------------------------

        itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=title,
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     fulltitle=title,
                     show=scrapedtitle))

    # Paginación
	next_page = re.compile('<link rel="next" href="(.+?)"/>', re.DOTALL).findall(data)
	for page in next_page:
		next_page = page
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR orange]Successivo >>[/COLOR]",
                     url=next_page,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist

def fichas(item):
    logger.info("[hdgratis.py] fichas")

    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare(item.url)
    # fix - calidad

    # ------------------------------------------------
    cookies = ""
    matches = re.compile('(.italiafilm.video.*?)\n', re.DOTALL).findall(config.get_cookie_data())
    for cookie in matches:
        name = cookie.split('\t')[5]
        value = cookie.split('\t')[6]
        cookies += name + "=" + value + ";"
    headers.append(['Cookie', cookies[:-1]])
    import urllib
    _headers = urllib.urlencode(dict(headers))
    # ------------------------------------------------

    patron = '<div class="col-mt-5 postsh">.*?'
    patron += 'href="([^"]+)".*?'
    patron += 'title="([^"]+)".*?'
    patron += '<img src="([^"]+)".*?'
       

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scraped_2, scrapedtitle, scrapedthumbnail in matches:

        scrapedurl = scraped_2
        


        title = scrapertools.decodeHtmlentities(scrapedtitle)
        # title += " (" + scrapedcalidad + ")

        # ------------------------------------------------
        scrapedthumbnail += "|" + _headers
        # ------------------------------------------------

        itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=title,
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     fulltitle=title,
                     show=scrapedtitle))

    # Paginación
	next_page = re.compile('<link rel="next" href="(.+?)"/>', re.DOTALL).findall(data)
	for page in next_page:
		next_page = page
    if next_page != "":
        itemlist.append(
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR orange]Successivo >>[/COLOR]",
                     url=next_page,
                     thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def findvideos(item):
    logger.info("[hdgratis.py] findvideos")

    itemlist = []

    # Descarga la página
    data = anti_cloudflare(item.url)

    patron = r'<iframe width=".+?" height=".+?" src="([^"]+)" allowfullscreen frameborder="0">'

    url = scrapertools.find_single_match(data, patron)

    if 'hdpass.link' in url:
        data = scrapertools.cache_page(url, headers=headers)

        start = data.find('<ul id="mirrors">')
        end = data.find('</ul>', start)
        data = data[start:end]

        patron = '<form method="get" action="">\s*'
        patron += '<input type="hidden" name="([^"]+)" value="([^"]+)"/>\s*'
        patron += '<input type="hidden" name="([^"]+)" value="([^"]+)"/>\s*'
        patron += '(?:<input type="hidden" name="([^"]+)" value="([^"]+)"/>\s*)?'
        patron += '<input type="submit" class="[^"]*" name="([^"]+)" value="([^"]+)"/>\s*'
        patron += '</form>'

        html = []
        for name1, val1, name2, val2, name3, val3, name4, val4 in re.compile(patron).findall(data):
            if name3 == '' and val3 == '':
                get_data = '%s=%s&%s=%s&%s=%s' % (name1, val1, name2, val2, name4, val4)
            else:
                get_data = '%s=%s&%s=%s&%s=%s&%s=%s' % (name1, val1, name2, val2, name3, val3, name4, val4)
            tmp_data = scrapertools.cache_page('http://hdpass.link/film.php?randid=0&' + get_data, headers=headers)

            patron = r'; eval\(unescape\("(.*?)",(\[".*?;"\]),(\[".*?\])\)\);'
            try:
                [(par1, par2, par3)] = re.compile(patron, re.DOTALL).findall(tmp_data)
            except:
                patron = r'<source src="([^"]+)"\s*type="video/mp4"(?:\s*data-res="([^"]+)")?'
                for media_url, media_label in re.compile(patron).findall(tmp_data):
                    itemlist.append(
                            Item(server='directo',
                                 action="play",
                                 title=' - [Player]' if media_label == '' else ' - [Player: quality %s]' % media_label,
                                 url=media_url,
                                 folder=False))
                continue

            par2 = eval(par2, {'__builtins__': None}, {})
            par3 = eval(par3, {'__builtins__': None}, {})
            tmp_data = unescape(par1, par2, par3)
            html.append(tmp_data.replace(r'\/', '/'))
        html = ''.join(html)
    else:
        html = url

    itemlist.extend(servertools.find_video_items(data=html))

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, videoitem.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.channel = __channel__

    return itemlist


def anti_cloudflare(url):
    try:
        resp_headers = scrapertools.get_headers_from_response(url, headers=headers)
        resp_headers = dict(resp_headers)
    except urllib2.HTTPError, e:
        resp_headers = e.headers

    if 'refresh' in resp_headers:
        import time
        time.sleep(int(resp_headers['refresh'][:1]))

        scrapertools.get_headers_from_response(host + "/" + resp_headers['refresh'][7:], headers=headers)

    return scrapertools.cache_page(url, headers=headers)


def unescape(par1, par2, par3):
    var1 = par1
    for ii in xrange(0, len(par2)):
        var1 = re.sub(par2[ii], par3[ii], var1)

    var1 = re.sub("%26", "&", var1)
    var1 = re.sub("%3B", ";", var1)
    return var1.replace('<!--?--><?', '<!--?-->')
