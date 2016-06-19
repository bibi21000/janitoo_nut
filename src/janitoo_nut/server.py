# -*- coding: utf-8 -*-

"""The NUT server

"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)
#logger.addHandler(NullHandler())
from threading import Thread, Event


from pkg_resources import get_distribution, DistributionNotFound
from janitoo.mqtt import MQTTClient
from janitoo.server import JNTServer

class NutServer(JNTServer):
    """The Nut Server

    """
    def _get_egg_path(self):
        """Return the egg path of the module. Must be redefined in server class. Used to find alembic migration scripts.
        """
        try:
            _dist = get_distribution('janitoo_nut')
            return _dist.__file__
        except AttributeError:
            return 'src-nut/config'

