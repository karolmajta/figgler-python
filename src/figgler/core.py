import re

FIG_ENV_REGEX = re.compile('^([A-Z0-9]+_)+\d+_PORT$')


def figvars(environ):
    pairs = filter(lambda p: re.match(FIG_ENV_REGEX, p[0]), environ.items())
    return dict(pairs)


def container_name(figvar):
    important_chunks = figvar.split('_')[:-2]
    return "_".join(map(lambda c: c.lower(), important_chunks))


def container_ordinal(figvar):
    return int(figvar.split('_')[-2])


def groupby_containers(figvars):
    containers = {}
    for k, v in figvars.items():
        container = container_name(k)
        ordinal = container_ordinal(k)
        l = containers.get(container, [])
        l.append({"value": v, "ordinal": ordinal})
        containers[container] = l
    for k, v in containers.items():
        v.sort(key=lambda v: v["ordinal"])
    for k in containers.keys():
        containers[k] = reduce(lambda memo, x: memo + [x["value"]], containers[k], [])
    return containers

class FigURI(object):
    """Simple value holder for URIs"""

    def __init__(self, uri):
        self.uri = uri
        self.protocol, rest = uri.split('://')
        self.host, self.port = rest.split(':')

    def __str__(self):
        d = {
            'uri': self.uri,
            'protocol': self.protocol,
            'host': self.host,
            'port': self.port
        }
        return str(d)

class Containers(object):
    """Simple value holder for containers"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = map(FigURI, v)