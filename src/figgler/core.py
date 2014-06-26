import re

FIG_ENV_REGEX = re.compile(r'^([A-Z0-9]+_)+\d+_PORT_\d+_TCP$')


def figvars(environ):
    pairs = filter(lambda p: re.match(FIG_ENV_REGEX, p[0]), environ.items())
    return dict(pairs)


def container_name(figvar):
    important_chunks = figvar.split('_')[:-4]
    return "_".join(map(lambda c: c.lower(), important_chunks))


def container_ordinal(figvar):
    return int(figvar.split('_')[-4])


def split_uri(uri):
    protocol, rest = uri.split('://')
    host, port = rest.split(':')
    return {'protocol': protocol, 'host': host, 'port': port}


def squash_ports(links):
    squashed = {}
    for link in links:
        k = (link['protocol'], link['host'])
        try:
            s = squashed[k]
        except KeyError:
            s = {'protocol': link['protocol'], 'host': link['host'], 'ports': []}
        s['ports'].append(link['port'])
        squashed[k] = s
    return squashed.values()


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
        containers[k] = map(split_uri, containers[k])
        containers[k] = squash_ports(containers[k])
    return containers


class FigURI(object):
    """Simple value holder for URIs"""

    def __init__(self, container):
        self.protocol = container['protocol']
        self.host = container['host']
        self.ports = container['ports']


class Containers(object):
    """Simple value holder for containers"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            for container_list in kwargs.values():
                for container in container_list:
                    tmp = map(int, container['ports'])
                    tmp.sort()
                    container['ports'] = map(str, tmp)
            self.__dict__[k] = map(FigURI, v)