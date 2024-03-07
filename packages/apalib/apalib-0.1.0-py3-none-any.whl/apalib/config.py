from apalib.Container import Container as Container
from apalib.Data import Data
Container = Container()
data = Data()


def ToStringLen(val, l, left_justify = True, truncate=True):
    if val is None:
        val = ''
    retstr = str(val)
    if len(retstr) < l and left_justify:
        retstr = retstr + " " * (l - len(retstr))
    elif len(retstr) < l and not left_justify:
        retstr = " " * (l - len(retstr)) + retstr
    if not truncate:
        return retstr
    else:
        return retstr[:l]
