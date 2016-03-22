# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC entry point
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# Constants
__plugin__  = "streamondemand"
__author__  = "iSOD"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/"
__date__ = "07/03/2016"
__version__ = "5.2.3"

import os
import sys

from core import config
from core import logger

logger.info("streamondemand.default init...")

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

# Runs xbmc launcher
from platformcode import launcher
launcher.run()
