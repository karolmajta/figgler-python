import os

from .core import figvars, groupby_containers, Containers


environ = figvars(os.environ)
containers = Containers(**groupby_containers(environ))