"""
****************
LED Array Module
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

__all__ = ["getArray", "getConfOptions"]

from common import update_dict

from modules.led.common import (
    CONF_KEY_NAME,
    CONF_KEY_OUTPUT,
    CONF_KEY_COUNT,
    CONF_KEY_PER_PIXEL,
    CONF_KEY_COLOR_ORDER,
    CONF_KEY_BRIGHTNESS,
    CONF_KEY_ANIM_FPS,
)
from modules.led.array import rpi, e131


def getArray(array_id, array_config, log):
    """
    Returns an LED Object or ``None`` if one is not available for the specified hardware.
    """
    array_classes = {}
    array_classes.update(rpi.SUPPORTED_TYPES)
    array_classes.update(e131.SUPPORTED_TYPES)
    clazz = array_classes.get(array_config[CONF_KEY_OUTPUT], None)

    if clazz:
        return clazz(
            id=array_id,
            name=array_config[CONF_KEY_NAME],
            count=array_config[CONF_KEY_COUNT],
            leds_per_pixel=array_config[CONF_KEY_PER_PIXEL],
            color_order=array_config[CONF_KEY_COLOR_ORDER],
            fps=array_config[CONF_KEY_ANIM_FPS],
            init_brightness=array_config[CONF_KEY_BRIGHTNESS],
            array_config=array_config,
        )
    else:
        log.error("No library is available for array '%s'", array_id)
    return None


def getConfOptions():
    """
    Return Conf Options from all array types
    """
    conf = {}
    conf = update_dict(conf, rpi.CONF_OPTIONS)
    conf = update_dict(conf, e131.CONF_OPTIONS)
    return conf