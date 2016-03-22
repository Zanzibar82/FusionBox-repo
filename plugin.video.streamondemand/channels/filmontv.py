# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para filmontv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re
import urllib

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "filmontv"
__category__ = "F"
__type__ = "generic"
__title__ = "filmontv.tv (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.comingsoon.it"

TIMEOUT_TOTAL = 60


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmontv mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR red]IN ONDA ADESSO[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/" % host,
                     thumbnail="http://a2.mzstatic.com/eu/r30/Purple/v4/3d/63/6b/3d636b8d-0001-dc5c-a0b0-42bdf738b1b4/icon_256.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Mattina[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=mt" % host,
                     thumbnail="http://www.creattor.com/files/23/787/morning-pleasure-icons-screenshots-17.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Pomeriggio[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=pm" % host,
                     thumbnail="http://icons.iconarchive.com/icons/custom-icon-design/weather/256/Sunny-icon.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Preserale[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=pr" % host,
                     thumbnail="https://s.evbuc.com/https_proxy?url=http%3A%2F%2Ftriumphbar.com%2Fimages%2Fhappyhour_icon.png&sig=ADR2i7_K2FSfbQ6b3dy12Xjgkq9NCEdkKg"),
                Item(channel=__channel__,
                     title="[COLOR azure]Prima serata[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=ps" % host,
                     thumbnail="http://icons.iconarchive.com/icons/icons-land/vista-people/256/Occupations-Pizza-Deliveryman-Male-Light-icon.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Seconda serata[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=ss" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Notte[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=nt" % host,
                     thumbnail="http://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/256/Status-weather-clear-night-icon.png")]

    return itemlist


def tvoggi(item):
    logger.info("streamondemand.filmontv tvoggi")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="col-xs-5 box-immagine">\s*<img src="([^"]+)"[^>]+>\s*</div>\s*[^>]+>[^>]+>\s*[^>]+>\s*[^>]+>(.*?)</div>\s*[^>]+>[^>]+>[^>]+>[^>]+>(.*?)</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedtv in matches:
        scrapedurl = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        titolo = urllib.quote_plus(scrapedtitle)
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
                Item(channel=__channel__,
                     action="do_search",
                     extra=titolo,
                     title=scrapedtitle + "[COLOR yellow]   " + scrapedtv + "[/COLOR]",
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     folder=True))

    return itemlist


# Esta es la función que realmente realiza la búsqueda

def do_search(item):
    logger.info("streamondemand.channels.buscador do_search")

    tecleado = item.extra
    mostra = item.fulltitle

    itemlist = []

    import os
    import glob
    import imp
    from lib.fuzzywuzzy import fuzz
    import threading
    import Queue
    import time
    import re

    master_exclude_data_file = os.path.join(config.get_runtime_path(), "resources", "sodsearch.txt")
    logger.info("streamondemand.channels.buscador master_exclude_data_file=" + master_exclude_data_file)

    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.py')
    logger.info("streamondemand.channels.buscador channels_path=" + channels_path)

    excluir = ""

    if os.path.exists(master_exclude_data_file):
        logger.info("streamondemand.channels.buscador Encontrado fichero exclusiones")

        fileexclude = open(master_exclude_data_file, "r")
        excluir = fileexclude.read()
        fileexclude.close()
    else:
        logger.info("streamondemand.channels.buscador No encontrado fichero exclusiones")
        excluir = "seriesly\nbuscador\ntengourl\n__init__"

    if config.is_xbmc():
        show_dialog = True

    try:
        import xbmcgui
        progreso = xbmcgui.DialogProgressBG()
        progreso.create("Ricerca di " + mostra)
    except:
        show_dialog = False

    def worker(infile, queue):
        channel_result_itemlist = []
        try:
            basename_without_extension = os.path.basename(infile)[:-3]
            # http://docs.python.org/library/imp.html?highlight=imp#module-imp
            obj = imp.load_source(basename_without_extension, infile)
            logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de " + infile)
            channel_result_itemlist.extend(obj.search(Item(), tecleado))
            for item in channel_result_itemlist:
                item.title = " [COLOR azure] " + item.title + " [/COLOR] [COLOR orange]su[/COLOR] [COLOR green]" + basename_without_extension + "[/COLOR]"
                item.viewmode = "list"
        except:
            import traceback
            logger.error(traceback.format_exc())
        queue.put(channel_result_itemlist)

    channel_files = [infile for infile in glob.glob(channels_path) if os.path.basename(infile)[:-3] not in excluir]

    result = Queue.Queue()
    threads = [threading.Thread(target=worker, args=(infile, result)) for infile in channel_files]

    start_time = int(time.time())

    for t in threads:
        t.daemon = True  # NOTE: setting dameon to True allows the main thread to exit even if there are threads still running
        t.start()

    number_of_channels = len(channel_files)
    completed_channels = 0
    while completed_channels < number_of_channels:

        delta_time = int(time.time()) - start_time
        if len(itemlist) <= 0:
            timeout = None  # No result so far,lets the thread to continue working until a result is returned
        elif delta_time >= TIMEOUT_TOTAL:
            break  # At least a result matching the searched title has been found, lets stop the search
        else:
            timeout = TIMEOUT_TOTAL - delta_time  # Still time to gather other results

        if show_dialog:
            progreso.update(completed_channels * 100 / number_of_channels)

        try:
            result_itemlist = result.get(timeout=timeout)
            completed_channels += 1
        except:
            # Expired timeout raise an exception
            break

        for item in result_itemlist:
            title = item.fulltitle

            # Clean up a bit the returned title to improve the fuzzy matching
            title = re.sub(r'\(.*\)', '', title)  # Anything within ()
            title = re.sub(r'\[.*\]', '', title)  # Anything within []

            # Check if the found title fuzzy matches the searched one
            if fuzz.WRatio(mostra, title) > 85: itemlist.append(item)

    if show_dialog:
        progreso.close()

    itemlist = sorted(itemlist, key=lambda item: item.fulltitle)

    return itemlist
