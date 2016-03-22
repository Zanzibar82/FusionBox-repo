# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Ricerca "Saghe"
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import base64
import datetime
import json
import re
import urllib

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "saghe"
__category__ = "F"
__type__ = "generic"
__title__ = "saghe"
__language__ = "IT"

DEBUG = config.get_setting("debug")

tmdb_key = 'f7f51775877e0bb6703520952b3c7840'
#tmdb_key = base64.urlsafe_b64decode('NTc5ODNlMzFmYjQzNWRmNGRmNzdhZmI4NTQ3NDBlYTk=')
dttime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
systime = dttime.strftime('%Y%m%d%H%M%S%f')
today_date = dttime.strftime('%Y-%m-%d')
month_date = (dttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
month2_date = (dttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
year_date = (dttime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
tmdb_image = 'http://image.tmdb.org/t/p/original'
tmdb_poster = 'http://image.tmdb.org/t/p/w500'


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.saghe mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR yellow]The Marvel Universe[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/50941077760ee35e1500000c?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/6t3KOEUtrIPmmtu1czzt6p2XxJy.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]The DC Comics Universe[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/5094147819c2955e4c00006a?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/xWlaTLnD8NJMTT9PGOD9z5re1SL.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]iMDb Top 250 Movies[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/522effe419c2955e9922fcf3?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/9O7gLzmreU0nGkIB6K3BsJbzvNv.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Rotten Tomatoes top 100 movies of all times[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/5418c914c3a368462c000020?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/zGadcmcF48gy8rKCX2ubBz2ZlbF.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Reddit top 250 movies[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/54924e17c3a3683d070008c8?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/dM2w364MScsjFf8pfMbaWUcWrR.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Sci-Fi Action[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/54408e79929fb858d1000052?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/5ig0kdWz5kxR4PHjyCgyI5khCzd.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]007 - Movies[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/557b152bc3a36840f5000265?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/zlWBxz2pTA9p45kUTrI8AQiKrHm.jpg"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Disney Classic Collection[/COLOR]",
                     action="tmdb_saghe",
                     url='http://api.themoviedb.org/3/list/51224e42760ee3297424a1e0?api_key=%s&language=it' % tmdb_key,
                     thumbnail="https://image.tmdb.org/t/p/w180_and_h270_bestv2/vGV35HBCMhQl2phhGaQ29P08ZgM.jpg"),
                Item( title="[COLOR azure]Hokuto no Ken[/COLOR]", channel="hokutonoken", action="mainlist", thumbnail="http://i.imgur.com/dn9ImTf.jpg"),
                Item( title="[COLOR azure]Saint Seiya[/COLOR]", channel="saintseiya" ,action="mainlist", thumbnail="http://vignette2.wikia.nocookie.net/nonciclopedia/images/1/12/Logo_Cavalieri_dello_Zodiaco.png/revision/latest?cb=20140308215438")]

    return itemlist



def tmdb_saghe(item):
    try:
        result = scrapertools.cache_page(item.url)
        result = json.loads(result)
        items = result['items']
    except:
        return

    itemlist = []
    for item in items:
        try:
            title = item['title']
            title = scrapertools.decodeHtmlentities(title)
            title = title.encode('utf-8')

            poster = item['poster_path']
            if poster == '' or poster is None:
                raise Exception()
            else:
                poster = '%s%s' % (tmdb_poster, poster)
            poster = poster.encode('utf-8')

            fanart = item['backdrop_path']
            if fanart == '' or fanart is None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (tmdb_image, fanart)
            fanart = fanart.encode('utf-8')

            plot = item['overview']
            if plot == '' or plot is None: plot = '0'
            plot = scrapertools.decodeHtmlentities(plot)
            plot = plot.encode('utf-8')

            itemlist.append(
                Item(channel=__channel__,
                     action="do_search",
                     extra=urllib.quote_plus(title),
                     title="[COLOR azure]%s[/COLOR]" % title,
                     fulltitle=title,
                     plot=plot,
                     thumbnail=poster,
                     fanart=fanart,
                     folder=True))
        except:
            pass

    return itemlist


def do_search(item):
    logger.info("streamondemand.channels.saghe do_search")

    tecleado = item.extra
    mostra = item.fulltitle

    itemlist = []

    import os
    import glob
    import imp
    from lib.fuzzywuzzy import fuzz
    import threading
    import Queue

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

    for t in threads:
        t.start()

    number_of_channels = len(channel_files)

    for index, t in enumerate(threads):
        percentage = index * 100 / number_of_channels
        if show_dialog:
            progreso.update(percentage, ' Sto cercando "' + mostra + '"')
        t.join()
        itemlist.extend(result.get())

    itemlist = sorted([item for item in itemlist if fuzz.WRatio(mostra, item.fulltitle) > 85],
                      key=lambda Item: Item.title)

    if show_dialog:
        progreso.close()

    return itemlist

