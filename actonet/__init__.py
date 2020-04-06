
__version__ = "0.1"

import sys

from .iface import ActoNet

from colomoto.minibn import BooleanNetwork

def load(bn):
    bn = BooleanNetwork.auto_cast(bn)
    return ActoNet(bn)


