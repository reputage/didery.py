"""
core package

flo behaviors

"""
import importlib

_modules = ['behaving', ]

for m in _modules:
    importlib.import_module(".{0}".format(m), package='diderypy.core')
