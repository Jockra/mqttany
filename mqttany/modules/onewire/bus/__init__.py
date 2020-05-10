"""
***********
OneWire Bus
***********

:Author: Michael Murton
"""
# Copyright (c) 2019-2020 MQTTany contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

from modules.onewire.bus.base import OneWireBus
from modules.onewire.bus import wire1

__all__ = [ "getBus", "getConfBusOptions", "getConfBusTypes" ]


def getBus(bus_type):
    """
    Returns a class for the bus based on bus type setting or ``None`` if
    one is not available.
    """
    if bus_type in wire1.CONF_BUS_SELECTION:
        return wire1.wire1()
    else:
        return None


def getConfBusOptions():
    """
    Returns all of the bus options to add to CONF_OPTIONS
    """
    options = {}
    options.update(wire1.CONF_OPTIONS)
    return options


def getConfBusTypes():
    """
    Returns all of the bus types to add to device selection
    """
    devices = []
    devices.extend(wire1.CONF_BUS_SELECTION)
    return devices


def validateAddress(address):
    """
    Validates a OneWire device address.
    Will remove any invalid characters and compute CRC if needed.
    Returns ``None`` if address is invalid.
    """
    return OneWireBus.validateAddress(address)