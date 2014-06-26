figgler-python
==============

# installation

## for production use

    $ pip install figgler

## for development

    $ git clone https://github.com/karolmajta/figgler-python.git
    $ cd figgler-python.git
    $ python setup.py test

# usage

You can just import `figgler` in your source code

    import figgler

Then you will have access to `figgler.environ` which is basically
a dict containing whatever environment variables related do containers
were injected into yours:

    >> import pprint
    >> pprint.pprint(figgler.environ)
    {'DB_1_PORT': 'tcp://172.17.0.3:5432',
     'DEMO_DB_1_PORT': 'tcp://172.17.0.3:5432',
     'DEMO_MONGO_1_PORT': 'tcp://172.17.0.5:27017',
     'DEMO_REDIS_1_PORT': 'tcp://172.17.0.4:6379',
     'MONGO_1_PORT': 'tcp://172.17.0.5:27017',
     'REDIS_1_PORT': 'tcp://172.17.0.4:6379'}

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
    >>> len(figgler.mysql)  # there is no link called mysql!
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Containers' object has no attribute 'mysql'

These list contains `FigURI` objects of which each has:

  - `uri` the full *uri* of container
  - `protocol` this is the *protocol* part of *uri* and most likely will
     be **tcp**
  - `host` the *host* this container can be reached at
  - `port` the *port* this container can be reached at

You can access them as regular object properties:

    >>> figgler.containers.db[0].uri
    tcp://172.17.0.3:5432
    >>> figgler.containers.db[0].protocol
    tcp
    >>> figgler.containers.db[0].host
    172.17.0.3
    >>> figgler.containers.db[0].port
    5432
    >>> # of course you can only reach as many containers of each type 
    ... # as many containers are running. By default fill will instument
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

For more info check out the demo directory of this repo. The only things you need
to run it are *docker* and *fig*.
