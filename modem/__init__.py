__author__ = 'Wijnand Modderman <maze@pyth0n.org>'
__copyright__ = [
                    'Copyright (c) 2010 Wijnand Modderman-Lenstra',
                    'Copyright (c) 1981 Chuck Forsberg'
                ]
__license__ = 'MIT'
__version__ = '0.2.4'

import gettext
from modem.protocol.xmodem import XModem
from modem.protocol.xmodem1k import XModem1K
from modem.protocol.xmodemcrc import XModemCrc
from modem.protocol.ymodem import YModem
from modem.protocol.zmodem import ZModem

gettext.install('modem')

# To satisfy import *
__all__ = [
    'XModem',
    'XModem1K',
    'XModemCrc',
    'YModem',
    'ZModem',
]
