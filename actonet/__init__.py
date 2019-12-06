
__version__ = "0.1"

from .iface import ActoNet

def load(bn):
    return ActoNet(bn)


