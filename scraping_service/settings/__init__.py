from .production import *

try:
    from .local_settings import *
except ImportError:
    print('Looks like no local file. You must be on production')