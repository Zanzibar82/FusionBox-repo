# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para youtube
# Buscador simple para visonar o descargar desde YouTube
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
#------------------------------------------------------------
import re, sys

from core import logger
from core import scrapertools
from core import jsontools
from core.item import Item

from platformcode import library

__channel__ = "youtube"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Buscar en YouTube"
__language__ = "ES"

## Normal page
page_url = "https://www.youtube.com/watch?v=%s"

## key
key0 = "AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA"
key1 = "AIzaSyDXWo8-scFY-Ugcn2A0vGo8023hpcWtXto"

## Googleapi search
api_search = "https://www.googleapis.com/youtube/v3/search" + \
             "?q=%s" + \
             "&regionCode=ES" + \
             "&part=snippet" + \
             "&hl=es_ES" + \
             "&key=" + key0 + \
             "&type=video" + \
             "&maxResults=%s" + \
             "&pageToken=%s"

## Googleapi video
api_video = "https://www.googleapis.com/youtube/v3/videos" + \
            "?part=snippet,contentDetails" + \
            "&id=%s" + \
            "&key=" + key0

### Arts
## thumbnails high (hq) 480x360
art_thumbnail = "https://i.ytimg.com/vi/%s/hqdefault.jpg"

## thumbnails standard (sd) 640x480
art_fanart = "https://i.ytimg.com/vi/%s/sddefault.jpg"

def isGeneric():
    return True

def mainlist(item):

    itemlist = []

    itemlist.append( Item( channel=__channel__, action="search", title="[COLOR azure]Cerca musica, trailers, concerti e spettacoli su [/COLOR]You[COLOR red]Tube[/COLOR] ...", thumbnail="http://i.klepeer.com/icons/you_tube_icon.png" ) )

    return itemlist

def search(item,texto):

    item.url = api_search % (texto, "50", "")

    try:
        return fichas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def fichas(item):

    itemlist = []

    texto = scrapertools.get_match( item.url, "search...([^&]+)&" )

    data = jsontools.load_json( scrapertools.cache_page( item.url ) )

    nextPageToken = data.get('nextPageToken')

    _items = data.get('items', {})

    for _item in _items:

        url = page_url % _item['id']['videoId']
        title = _item['snippet']['title']
        plot = _item['snippet']['description']
        thumbnail = art_thumbnail % _item['id']['videoId']
        fanart = art_thumbnail % _item['id']['videoId']

        fulltitle = title
        title = scrapertools.htmlclean( title )
        show = library.title_to_folder_name( title )
        plot = scrapertools.htmlclean( plot )

        itemlist.append( Item( channel=__channel__, title=title, url=url, action="play", thumbnail=thumbnail, fanart=fanart, plot=plot, server="youtube", fulltitle=fulltitle, viewmode="movie_with_plot", show=show, folder=False ) )

    ## Paginación
    url = api_search % (texto, "50", nextPageToken)
    itemlist.append( Item( channel=__channel__, title="Pagina successiva >>", url=url, action="fichas", folder=True ) )

    return itemlist
