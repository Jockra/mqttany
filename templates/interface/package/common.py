"""
*************************
Interface Module Template
*************************

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

__all__ = [
    "log",
    "CONFIG",
    "publish_queue",
    "nodes",
    "CONF_KEY_STRING",
    "CONF_KEY_FIXED_TYPE",
    "CONF_KEY_SELECTION",
    "CONF_KEY_SUBSECTION",
    "CONF_OPTIONS",
]

from collections import OrderedDict

import logger

# If you don't specify the logging name you will get `interface_pkg_template.common` here
log = logger.get_logger("interface_pkg_template")
CONFIG = {}

# If the module publishes messages it must have the `publish_queue` attribute. It will
# be assigned a queue that the module can use `put_nowait()` to put BusMessage objects
# in the queue to be transmitted by the communication modules.
# Omit this if module is subscribe only
publish_queue = None
"""
When using this in other files in this package you MUST use it like this:
    from modules.interface_pkg_template import common
    common.publish_queue.put_nowait(BusMessage(...))

You must NOT import it and use it like this:
    from modules.interface_pkg_template.common import publish_queue
    publish_queue.put_nowait(BusMessage(...))

The problem comes from the fact 'publish_queue' is assigned at run time. When the module
is loaded it has a value of 'None', but is later assigned a queue. If you import it
directly into the namespace of a file you get a copy of value because 'NoneType' is a
simple object. This would not be a problem if we were assigning it a queue at load time,
because a queue (class instance) is a complex object. When you import a complex object
into a file's namespace you get a reference to where the object is stored, thus both the
file's 'publish_queue' and the 'publish_queue' in common refer to the same object. By
using the 'mprop' library to assign the queue given to the module by core to the
'publish_queue' attribute of the 'common' file, we can access it from the rest of the
files in the package as long as we reference the 'common' file's copy of it like
'common.publish_queue'.
"""


# Interface modules must have a non-empty dict of Nodes that they provide. This can be
# partially or entirely populated at runtime in the `load` function.
nodes = {}

# Configuration keys, best to define them here so they can be changed easily
CONF_KEY_STRING = "string"
CONF_KEY_FIXED_TYPE = "fixed type"
CONF_KEY_SELECTION = "selection"
CONF_KEY_SUBSECTION = "sub section"

# Configuration layout for `parse_config`
# it should be an OrderedDict of `(key, {})`
CONF_OPTIONS = OrderedDict(
    [
        (  # an empty dict means any value is valid and option is required
            CONF_KEY_STRING,
            {},
        ),
        (  # fixed type options should provide a type to compare with
            CONF_KEY_FIXED_TYPE,
            {
                # if a `default` is given the option is assumed to be optional
                "type": int,
                "default": 200,
                "secret": True,  # This will cause the value to appear as *'s in the log
            },
        ),
        (  # subsections are also possible
            CONF_KEY_SUBSECTION,
            {
                # they must have type set to "section"
                "type": "section",
                # if a subsection is optional you must specify this, if this
                # is omitted the subsection is assumed to be required.
                "required": False,
                CONF_KEY_SELECTION: {
                    # you can limit the possible values by providing a list or dict of
                    # possibilities. The config will be invalid if the value is not in
                    # "selection". If "selection" is a dict then the key's value will be
                    # returned, not the key.
                    "default": None,
                    "selection": {"option 1": 1, "option 2": 2},
                },
            },
        ),
        (  # regex pattern sections can also be used, their key must be "regex:{pattern}"
            # when using regex sections that may match other keys they should be last
            # and CONF_OPTIONS
            "regex:pattern",
            {"type": "section"},
        ),
    ]
)