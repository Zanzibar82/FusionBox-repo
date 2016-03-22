# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para novedades
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------

from core import config
from core import logger
from core.item import Item

__channel__ = "novedades"
__category__ = "F"
__type__ = "generic"
__title__ = "Novedades"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item, preferred_thumbnail="squares"):
    logger.info("streamondemand.channels.novedades mainlist")

    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="Film 3D - (Scegliere 2° server)",
                     thumbnail="http://media.tvalacarta.info/streamondemand." + preferred_thumbnail + "/thumb_canales_peliculas.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="peliculas_infantiles",
                     title="Per Bambini",
                     thumbnail="http://media.tvalacarta.info/streamondemand." + preferred_thumbnail + "/thumb_canales_infantiles.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="series",
                     title="Episodi di Serie TV",
                     thumbnail="http://media.tvalacarta.info/streamondemand." + preferred_thumbnail + "/thumb_canales_series.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="anime",
                     title="Episodi di Anime",
                     thumbnail="http://media.tvalacarta.info/streamondemand." + preferred_thumbnail + "/thumb_canales_anime.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="documentales",
                     title="Documentari",
                     thumbnail="http://media.tvalacarta.info/streamondemand." + preferred_thumbnail + "/thumb_canales_documentales.png",
                     viewmode="movie")]

    return itemlist


def peliculas(item):
    logger.info("streamondemand.channels.novedades peliculas")

    itemlist = []

    import portalehd
    item.url = "http://www.portalehd.net/category/3d/"
    itemlist.extend(portalehd.peliculas(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def peliculas_infantiles(item):
    logger.info("streamondemand.channels.novedades peliculas_infantiles")

    itemlist = []

    import guardaserie
    item.url = "http://www.guardaserie.net/lista-serie-tv-guardaserie/"
    itemlist.extend(guardaserie.cartoni(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def series(item):
    logger.info("streamondemand.channels.novedades series")

    itemlist = []

    # import serietvsubita
    # item.url = "http://serietvsubita.net/"
    # itemlist.extend( serietvsubita.episodios(item) )

    import guardaserie
    item.url = "http://www.guardaserie.net/lista-serie-tv-guardaserie/"
    itemlist.extend(guardaserie.fichas(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def anime(item):
    logger.info("streamondemand.channels.novedades anime")

    itemlist = []

    import animesubita
    item.url = "ttp://www.animesubita.info/"
    itemlist.extend(animesubita.novedades(item))

    import cineblog01
    item.url = "http://www.cineblog01.cc/anime/"
    itemlist.extend(cineblog01.listanime(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.endswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def documentales(item):
    logger.info("streamondemand.channels.novedades documentales")

    itemlist = []

    import documentaristreaming
    item.url = "http://documentaristreaming.net/"
    itemlist.extend(documentaristreaming.peliculas(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist
