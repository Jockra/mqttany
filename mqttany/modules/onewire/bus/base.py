"""
****************
OneWire Bus Base
****************

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

import re

re_hex_chars = re.compile("[^a-fA-F0-9]")

__all__ = ["OneWireBus"]


class OneWireBus:
    """
    OneWire Bus base class
    """

    def __init__(self):
        pass

    @staticmethod
    def validateAddress(address):
        """
        Validates a OneWire device address.
        Will remove any invalid characters and compute CRC if needed.
        Returns ``None`` if address is invalid.
        """
        s = re_hex_chars.sub("", str(address))
        if len(s) == 16:
            return s.upper()
        elif len(s) == 14:
            return str(s + OneWireBus.crc8(bytes.fromhex(s)).hex()).upper()
        else:
            return None

    @staticmethod
    def crc8(data):
        """
        Returns 1 byte CRC-8/MAXIM of the contents of bytes ``data``.
        """
        crc = 0
        for i in range(len(data)):
            byte = data[i]
            for bit in range(8):
                mix = (crc ^ byte) & 0x01
                crc >>= 1
                if mix:
                    crc ^= 0x8C
                byte >>= 1
        return bytes([crc])

    def scan(self):
        """
        Scan bus and return list of addresses found.
        """
        raise NotImplementedError

    def read(self, address, length):
        """
        Read ``length`` bytes from device (not including crc8).
        """
        raise NotImplementedError

    def write(self, address, buffer):
        """
        Write ``bytes`` to device (not including crc8).
        """
        raise NotImplementedError

    @property
    def valid(self):
        """
        Returns ``True`` if the bus is available.
        """
        raise NotImplementedError
