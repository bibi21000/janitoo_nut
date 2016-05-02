# -*- coding: utf-8 -*-
"""The Nut Janitoo helper

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

import os, sys
from datetime import datetime, timedelta
from nut2 import PyNUTClient
import threading

from janitoo.thread import JNTBusThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD, HADD_SEP, json_dumps, json_loads
from janitoo.node import JNTNode
from janitoo.value import JNTValue, value_config_poll
from janitoo.bus import JNTBus
from janitoo.component import JNTComponent

OID = 'nut'

def make_thread(options):
    if get_option_autostart(options, 'nut') == True:
        return NutThread(options)
    else:
        return None

def make_ups(**kwargs):
    return NutUps(**kwargs)

class NutThread(JNTBusThread):
    """The Nut thread&

    """
    def init_bus(self):
        """Build the bus
        """
        self.section = 'nut'
        self.bus = JNTBus(options=self.options, oid=self.section, product_name="NUT controller")

class NutUps(JNTComponent):
    """
    This class abstracts a roowifi and gives attributes for telemetry data,
    as well as methods to command the robot
    """
    def __init__(self, bus=None, addr=None, **kwargs):
        JNTComponent.__init__(self,
            oid = kwargs.pop('oid', '%s.ups'%OID),
            bus = bus,
            addr = addr,
            name = kwargs.pop('name', "NUT Ups"),
            product_name = kwargs.pop('product_name', "NUT Ups"),
            **kwargs)
        self._lock =  threading.Lock()
        self._battery_charge = -1.0
        self._battery_voltage = -1.0
        self._battery_runtime = -1.0
        self._battery_chemistry = "unknown"
        self._status = "unknown"
        self._ups_stats_last = False
        self._ups_stats_next_run = datetime.now() + timedelta(seconds=10)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

        uuid="ip_ping"
        self.values[uuid] = self.value_factory['ip_ping'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Ping the nut server',
            label='Ping',
            default='127.0.0.1'
        )
        config_value = self.values[uuid].create_config_value(help='The IP of the NUT server', label='IP',)
        self.values[config_value.uuid] = config_value
        poll_value = self.values[uuid].create_poll_value()
        self.values[poll_value.uuid] = poll_value

        uuid="username"
        self.values[uuid] = self.value_factory['config_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Username to connect the nut server',
            label='Username',
        )

        uuid="upsname"
        self.values[uuid] = self.value_factory['config_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Ups name on the nut server',
            label='UPS',
        )

        uuid="password"
        self.values[uuid] = self.value_factory['config_password'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Password to connect the nut server',
            label='Password',
        )

        uuid="port"
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Port to connect the nut server',
            label='Port',
            default=3493,
        )

        uuid="battery_voltage"
        self.values[uuid] = self.value_factory['sensor_voltage'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The voltage of the battery',
            label='Voltage',
            get_data_cb=self.get_battery_voltage,
        )
        poll_value = self.values[uuid].create_poll_value(default=90)
        self.values[poll_value.uuid] = poll_value

        uuid="battery_charge"
        self.values[uuid] = self.value_factory['sensor_percent'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The charge of the battery',
            label='Charge',
            get_data_cb=self.get_battery_charge,
        )
        poll_value = self.values[uuid].create_poll_value(default=90)
        self.values[poll_value.uuid] = poll_value

        uuid="battery_chemistry"
        self.values[uuid] = self.value_factory['sensor_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The chemistry of the battery',
            label='Chemistry',
            get_data_cb=self.get_battery_chemistry,
        )
        poll_value = self.values[uuid].create_poll_value(default=1800)
        self.values[poll_value.uuid] = poll_value

        uuid="battery_runtime"
        self.values[uuid] = self.value_factory['sensor_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The left runtime of the battery',
            label='Runtime',
            units='Seconds',
            get_data_cb=self.get_battery_runtime,
        )
        poll_value = self.values[uuid].create_poll_value(default=90)
        self.values[poll_value.uuid] = poll_value

        uuid="status"
        self.values[uuid] = self.value_factory['sensor_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The status of the UPS',
            label='Status',
            get_data_cb=self.get_status,
        )
        poll_value = self.values[uuid].create_poll_value(default=60)
        self.values[poll_value.uuid] = poll_value

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        #~ print "it's me %s : %s" % (self.values['upsname'].data, self._ups_stats_last)
        return self._ups_stats_last

    def get_ups_stats(self):
        """
        """
        ret = False
        if self._ups_stats_next_run < datetime.now():
            locked = self._lock.acquire(False)
            if locked == True:
                try:
                    client = PyNUTClient(host=self.values['ip_ping_config'].data,login=self.values['username'].data, password=self.values['password'].data, port=self.values['port'].data)
                    res = client.list_vars(self.values['upsname'].data)
                    self._battery_charge = res['battery.charge']
                    self._battery_voltage = res['battery.voltage']
                    self._battery_runtime = res['battery.runtime']
                    self._battery_chemistry = res['battery.chemistry']
                    self._status = res['ups.status']
                    self.node.product_name = res['ups.model']
                    self.node.product_type = res['ups.serial']
                    self.node.product_manufacturer = res['ups.mfr']
                    self._ups_stats_last = True
                    ret = True
                except:
                    logger.exception("[%s] - Exception catched in get_ups_stats", self.__class__.__name__)
                    self._ups_stats_last = False
                finally:
                    self._lock.release()
                    logger.debug("And finally release the lock !!!")
                if self.values['ip_ping_poll'].data>0:
                    self._ups_stats_next_run = datetime.now() + timedelta(seconds=self.values['ip_ping_poll'].data)
            return ret
        return False

    def get_battery_charge(self, node_uuid, index):
        """Return the battery charge
        """
        self.get_ups_stats()
        return self._battery_charge

    def get_battery_voltage(self, node_uuid, index):
        """Return the battery voltage
        """
        self.get_ups_stats()
        return self._battery_voltage

    def get_battery_chemistry(self, node_uuid, index):
        """Return the battery chemistry
        """
        self.get_ups_stats()
        return self._battery_chemistry

    def get_battery_runtime(self, node_uuid, index):
        """Return the battery runtime
        """
        self.get_ups_stats()
        return self._battery_runtime

    def get_status(self, node_uuid, index):
        """Return the status
        """
        self.get_ups_stats()
        return self._status
