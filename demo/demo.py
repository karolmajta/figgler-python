import pprint

import figgler

print
print "-----------------------"
print "Welcome to figgler demo"
print "-----------------------"
print
print "Fig environment is:"
pprint.pprint(figgler.environ)
print
print "There are {0} database containers:".format(len(figgler.containers.db))
for db_container in figgler.containers.db:
    print "-", db_container
print
print "There are {0} redis containers:".format(len(figgler.containers.redis))
for redis_container in figgler.containers.redis:
    print "-", redis_container
print
print "There are {0} mongo containers:".format(len(figgler.containers.mongo))
for mongo_container in figgler.containers.mongo:
    print "-", mongo_container
print
print "-----------------------------------------------------------------------"
print "Thanks for using figgler (https://github.com/karolmajta/figgler-python)"
print "-----------------------------------------------------------------------"
print
