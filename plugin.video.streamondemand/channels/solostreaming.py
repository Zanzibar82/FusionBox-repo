# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per solo-streaming.com
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import json
import sys
import urllib
from unicodedata import normalize

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "solostreaming"
__category__ = "S"
__type__ = "generic"
__title__ = "solostreaming"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://solo-streaming.com"
result_per_page = 25


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.solostreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[B][COLOR royalblue][SERIE TV][/COLOR][/B] [B][COLOR deepskyblue]ULTIMI EPISODI AGGIORNATI[/COLOR][/B]",
                     action="updateserietv",
                     url="%s/sod/api.php?get=serietv&type=elenco&order=multi&days=30&start=0&end=%d" % (
                     host, result_per_page),
                     extra="serietv",
                     thumbnail="http://solo-streaming.com/images/sod/serietv1_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR royalblue][SERIE TV][/COLOR][/B] [B][COLOR deepskyblue]AGGIORNAMENTI MENSILI[/COLOR][/B]",
                     action="dailyupdateserietv",
                     url="%s/sod/api.php?get=serietv&type=elenco&order=multi&days=30" % host,
                     extra="serietv",
                     thumbnail="http://solo-streaming.com/images/sod/serietv2_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR royalblue][SERIE TV][/COLOR][/B] [B][COLOR deepskyblue]ELENCO COMPLETO SERIE TV[/COLOR][/B]",
                     action="elencoserie",
                     extra="serietv",
                     thumbnail="http://solo-streaming.com/images/sod/serietv3_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR royalblue][SERIE TV][/COLOR][/B] [B][COLOR deepskyblue]CERCA...[/COLOR][/B]",
                     action="search",
                     extra="serie",
                     thumbnail="http://solo-streaming.com/images/sod/serietv4_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR springgreen][ANIME][/COLOR][/B] [B][COLOR deepskyblue]ULTIMI EPISODI AGGIORNATI[/COLOR][/B]",
                     action="updateserietv",
                     url="%s/sod/api.php?get=anime&type=elenco&order=multi&days=30&start=0&end=%d" % (
                     host, result_per_page),
                     extra="anime",
                     thumbnail="http://solo-streaming.com/images/sod/anime1_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR springgreen][ANIME][/COLOR][/B] [B][COLOR deepskyblue]AGGIORNAMENTI MENSILI[/COLOR][/B]",
                     action="dailyupdateserietv",
                     url="%s/sod/api.php?get=anime&type=elenco&order=multi&days=30" % host,
                     extra="anime",
                     thumbnail="http://solo-streaming.com/images/sod/anime2_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR springgreen][ANIME][/COLOR][/B] [B][COLOR deepskyblue]ELENCO COMPLETO ANIME[/COLOR][/B]",
                     action="elencoserie",
                     extra="anime",
                     thumbnail="http://solo-streaming.com/images/sod/anime3_225x330.jpg"),
                Item(channel=__channel__,
                     title="[B][COLOR springgreen][ANIME][/COLOR][/B] [B][COLOR deepskyblue]CERCA...[/COLOR][/B]",
                     action="search",
                     extra="anime",
                     thumbnail="http://solo-streaming.com/images/sod/anime4_225x330.jpg")
                ]

    return itemlist


def elencoserie(item):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    apielenco = "%s/sod/api.php?get=%s&type=elenco&order=alphabetic&letter=%s&start=0&end=%d"
    itemlist = []
    for letter in alphabet:
        frm_title = "[B][COLOR deepskyblue]%s[/COLOR][/B]" % letter.upper()
        itemlist.append(
            Item(channel=__channel__,
                 action="elencoserieletter",
                 title=frm_title,
                 url=apielenco % (host, item.extra, letter, result_per_page),
                 thumbnail=item.thumbnail,
                 fulltitle=frm_title,
                 extra=item.extra,
                 show=frm_title))

    return itemlist


def elencoserieletter(item):
    itemlist = []

    # Descarga la pagina
    data = cache_jsonpage(item.url)

    for singledata in data['results']:

        if item.extra == 'serietv':
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serieNome'])).strip()
        else:
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serie'])).strip()

        scrapedplot = ""
        frm_title = "[B][COLOR deepskyblue]%s[/COLOR][/B]" % serie
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=serie,
                 show=serie,
                 title=frm_title,
                 url=singledata['uri'] + '||' + item.extra,
                 thumbnail=singledata['fileName'],
                 plot=scrapedplot,
                 folder=True))

    itemlist.append(
        Item(channel=__channel__,
             action="HomePage",
             title="[COLOR yellow]Torna Home[/COLOR]",
             folder=True))

    if len(data['results']) == result_per_page:
        end = int(scrapertools.find_single_match(item.url, r"&end=(\d+)"))
        next_page = item.url.split('&start=')[0] + "&start=%d&end=%d" % (end, end + result_per_page)

        itemlist.append(
            Item(channel=__channel__,
                 action="elencoserieletter",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def cache_jsonpage(url):
    return json.loads(scrapertools.cache_page(url))


def dailyupdateserietv(item):
    logger.info("streamondemand.solostreaming dailyupdateserietv")

    itemlist = []

    # Descarga la pagina
    data = cache_jsonpage(item.url)

    dailyupdate = {}
    for singledata in data['results']:
        key = singledata['created']
        if key not in dailyupdate:
            dailyupdate[key] = []
        dailyupdate[key].append(singledata)

    for key in sorted(dailyupdate, reverse=True):
        scrapedplot = ""

        value = dailyupdate[key]

        extra = json.dumps(value)

        frm_title = "[B][COLOR deepskyblue]%s-%s-%s[/COLOR][/B] [COLOR white](%d serie aggiornate)[/COLOR]" % (
        key[8:], key[5:7], key[:4], len(value))

        itemlist.append(
            Item(channel=__channel__,
                 action="showupdateserietv",
                 fulltitle=frm_title,
                 show=frm_title,
                 title=frm_title,
                 url=item.extra,
                 thumbnail="",
                 extra=extra,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def showupdateserietv(item):
    logger.info("streamondemand.solostreaming showupdateserietv")

    extra = json.loads(item.extra)

    itemlist = []

    for singledata in extra:
        scrapedplot = ""

        type = normalize_unicode(singledata['type'])
        uri = normalize_unicode(singledata['uri'])

        if item.url == 'serietv':
            ep_num = normalize_unicode(singledata['ep_num'])
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serieNome'])).strip()
            titolo = scrapertools.decodeHtmlentities(normalize_unicode(singledata['ep_title'])).strip()

            apisingle = host + "/sod/api.php?get=serietv&type=episodi&uri=" + uri + "&ep_num=" + ep_num + "&sub=" + urllib.quote_plus(
                type)

            frm_title = "[COLOR white](%s)[/COLOR] [B][COLOR royalblue]%s[/COLOR][/B] [B][COLOR deepskyblue]- %s %s[/COLOR][/B]" % (
            type.upper(), serie, ep_num, titolo)
        else:
            e_num = normalize_unicode(singledata['e_num'])
            s_num = normalize_unicode(singledata['s_num'])
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serie'])).strip()

            apisingle = host + "/sod/api.php?get=anime&type=episodi&uri=" + uri + "&e_num=" + e_num + "&s_num=" + s_num + "&sub=" + urllib.quote_plus(
                type)

            frm_title = "[COLOR white](%s)[/COLOR] [B][COLOR royalblue]%s[/COLOR][/B] [B][COLOR deepskyblue]- %sx%s[/COLOR][/B]" % (
            type.upper(), serie, s_num, e_num)

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 fulltitle=frm_title,
                 show=frm_title,
                 title=frm_title,
                 url=apisingle,
                 thumbnail=singledata['fileName']))

    itemlist.append(
        Item(channel=__channel__,
             action="HomePage",
             title="[COLOR yellow]Torna Home[/COLOR]"))

    return itemlist


def updateserietv(item):
    logger.info("streamondemand.solostreaming update serietv")

    itemlist = []

    # Descarga la pagina
    data = cache_jsonpage(item.url)

    for singledata in data['results']:

        type = normalize_unicode(singledata['type'])
        uri = normalize_unicode(singledata['uri'])
        if item.extra == 'serietv':
            ep_num = normalize_unicode(singledata['ep_num'])
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serieNome'])).strip()
            titolo = scrapertools.decodeHtmlentities(normalize_unicode(singledata['ep_title'])).strip()

            apisingle = host + "/sod/api.php?get=serietv&type=episodi&uri=" + uri + "&ep_num=" + ep_num + "&sub=" + urllib.quote_plus(
                type)

            frm_title = "[COLOR white](%s)[/COLOR] [B][COLOR royalblue]%s[/COLOR][/B] [B][COLOR deepskyblue]- %s %s[/COLOR][/B]" % (
            type.upper(), serie, ep_num, titolo)
        else:
            e_num = normalize_unicode(singledata['e_num'])
            s_num = normalize_unicode(singledata['s_num'])
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serie'])).strip()

            apisingle = host + "/sod/api.php?get=anime&type=episodi&uri=" + uri + "&e_num=" + e_num + "&s_num=" + s_num + "&sub=" + urllib.quote_plus(
                type)

            frm_title = "[COLOR white](%s)[/COLOR] [B][COLOR royalblue]%s[/COLOR][/B] [B][COLOR deepskyblue]- %sx%s[/COLOR][/B]" % (
            type.upper(), serie, s_num, e_num)

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 fulltitle=frm_title,
                 show=frm_title,
                 title=frm_title,
                 url=apisingle,
                 thumbnail=singledata['fileName']))

    itemlist.append(
        Item(channel=__channel__,
             action="HomePage",
             title="[COLOR yellow]Torna Home[/COLOR]"))

    if len(data['results']) == result_per_page:
        end = int(scrapertools.find_single_match(item.url, r"&end=(\d+)"))
        next_page = item.url.split('&start=')[0] + "&start=%d&end=%d" % (end, end + result_per_page)

        itemlist.append(
            Item(channel=__channel__,
                 action="updateserietv",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def serietv(item):
    logger.info("streamondemand.solostreaming serietv")

    itemlist = []

    # Descarga la pagina
    data = cache_jsonpage(item.url)

    for singledata in data['results']:
        if item.extra == 'serietv':
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serieNome'])).strip()
        else:
            serie = scrapertools.decodeHtmlentities(normalize_unicode(singledata['serie'])).strip()

        frm_title = "[B][COLOR deepskyblue]%s[/COLOR][/B]" % serie
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=serie,
                 show=serie,
                 title=frm_title,
                 url=singledata['uri'] + '||' + item.extra,
                 thumbnail=singledata['fileName'],
                 plot=scrapedplot,
                 folder=True))

    itemlist.append(
        Item(channel=__channel__,
             action="HomePage",
             title="[COLOR yellow]Torna Home[/COLOR]",
             folder=True))

    if len(data['results']) == result_per_page:
        end = int(scrapertools.find_single_match(item.url, r"&end=(\d+)"))
        next_page = item.url.split('&start=')[0] + "&start=%d&end=%d" % (end, end + result_per_page)

        itemlist.append(
            Item(channel=__channel__,
                 action="serietv",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")


def search(item, texto):
    logger.info("[solostreaming.py] " + item.url + " search " + texto)

    if item.extra == 'serie':
        item.url = "%s/sod/api.php?get=serietv&type=data&serie=%s&start=0&end=%d" % (host, texto, result_per_page)
        item.extra = 'serietv'
    else:
        item.url = "%s/sod/api.php?get=anime&type=data&serie=%s&start=0&end=%d" % (host, texto, result_per_page)
        item.extra = 'anime'

    try:
        return serietv(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def episodios(item):
    logger.info("[solostreaming.py] episodios")

    itemlist = []

    # Descarga la página
    hosturi = "%s/sod/api.php?get=%s&type=episodi&uri=%s" % (host, item.url.split('||')[1], item.url.split('||')[0])
    data = cache_jsonpage(hosturi)

    for singledata in data:
        type = normalize_unicode(singledata['type'])
        if item.extra == 'serietv':
            titolo = scrapertools.decodeHtmlentities(normalize_unicode(singledata['ep_title'])).strip()
            ep_num = normalize_unicode(singledata['ep_num'])

            frm_title = "[COLOR white](%s) [B][COLOR deepskyblue]- %s %s[/COLOR][/B]" % (type.upper(), ep_num, titolo)
        else:
            e_num = normalize_unicode(singledata['e_num'])
            s_num = normalize_unicode(singledata['s_num'])

            frm_title = "[COLOR white](%s) [B][COLOR deepskyblue]- %sx%s[/COLOR][/B]" % (type.upper(), s_num, e_num)

        links = ' '.join(singledata['links'])

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title=frm_title,
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=links,
                 fulltitle=item.fulltitle,
                 show=item.show))

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


def findvid_serie(item):
    logger.info("[solostreaming.py] findvideos")

    # Descarga la página
    if item.extra != "":
        data = item.extra
    else:
        data = cache_jsonpage(item.url)
        data = ' '.join(data[0]['links'])

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist


def normalize_unicode(string, encoding='utf-8'):
    if string is None: string = ''
    return normalize('NFKD', string if isinstance(string, unicode) else unicode(string, encoding, 'ignore')).encode(
        encoding, 'ignore')
