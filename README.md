figgler-python
==============

**figgler-python** is an utility for providing seamless experience
when detecting cooperating docker containers when running fig-instrumented
python applications.

# installation

## for production use

    $ pip install figgler

## for development

    $ git clone https://github.com/karolmajta/figgler-python.git
    $ cd figgler-python.git
    $ pip install -r requirements.txt
    $ invoke unittest  # to run tests and check if everything is fine
    $ invoke watch     # to start a file watcher and do some awesome changes

# usage

You can just import `figgler` in your source code

    import figgler

Then you will have access to `figgler.environ` which is basically
a dict containing whatever environment variables related do containers
were injected into yours:

    >> import pprint
    >> pprint.pprint(figgler.environ)
    {'DB_1_PORT_5432_TCP': 'tcp://172.17.0.18:5432',
     'DEMO_DB_1_PORT_5432_TCP': 'tcp://172.17.0.18:5432',
     'DEMO_MONGO_1_PORT_27017_TCP': 'tcp://172.17.0.20:27017',
     'DEMO_MONGO_1_PORT_28017_TCP': 'tcp://172.17.0.20:28017',
     'DEMO_REDIS_1_PORT_6379_TCP': 'tcp://172.17.0.19:6379',
     'MONGO_1_PORT_27017_TCP': 'tcp://172.17.0.20:27017',
     'MONGO_1_PORT_28017_TCP': 'tcp://172.17.0.20:28017',
     'REDIS_1_PORT_6379_TCP': 'tcp://172.17.0.19:6379'}

`figgler` object exposes `figgler.containers` which will resemble
whatever links were configured in your `fig.yml`, for example
given your figfile looks like this:

    db:
      image: orchardup/postgresql
    redis:
      image: dockerfile/redis
    mongo:
      image: dockerfile/mongodb
    app:
      image: dockerfile/python
      command: bash -c "pip install -r requirements.txt && python demo.py"
      volumes:
        - .:/data
      links:
        - db
        - redis
        - mongo

You will be able to access `figgler.containers.db`, `figgler.containers.mongo`
and `figgler.containers.redis`:

    >>> len(figgler.containers.mongo)
    1
    >>> len(figgler.containers.db)
    1
    >>> len(figgler.mysql  # there is no link called mysql!
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Containers' object has no attribute 'mysql'

These list contains `FigURI` objects of which each has:

  - `protocol` this is the *protocol* part of *uri* and most likely will
     be **tcp**
  - `host` the *host* this container can be reached at
  - `ports` the list of *ports* this container can be reached at, sorted ascending

You can access them as regular object properties:

    >>> figgler.containers.db[0].protocol
    tcp
    >>> figgler.containers.db[0].host
    172.17.0.3
    >>> figgler.containers.db[0].ports
    ['5432']
    >>> # of course you can only reach as many containers of each type 
    ... # as many containers are running. By default fig will instument
    ... # one of each type, so we only have one `mongo` container in the list
    ...
    >>> figgler.containers.mongo[1]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: list index out of range    

Of course you can try it with more containers of each type. Run two terminals,
in first do:

    $ fig up db=1 redis=2 mongo=2

Then run your app container in which you can get:

    >>> figgler.containers.redis[1].host
    172.17.0.8
    >>> figgler.containers.mongo[1].ports
    ['27017', '28017']
    >>> # note that mongo container exposes two ports, and they are both
    ... # available in the list

For more info check out the demo directory of this repo. The only things you need
to run it are *docker* and *fig*.
