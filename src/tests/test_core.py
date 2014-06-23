import unittest

from figgler.core import FIG_ENV_REGEX, figvars, FigURI, container_name, groupby_containers, \
    container_ordinal, Containers


class FigenvRegexTestCase(unittest.TestCase):

    def testMatchesFirstInstance(self):
        self.assertRegexpMatches('DB_1_PORT', FIG_ENV_REGEX)

    def testMatchesNthInstance(self):
        self.assertRegexpMatches('DB_28_PORT', FIG_ENV_REGEX)

    def testMatchesNamesWithUnerscores(self):
        self.assertRegexpMatches('MONGO_DB_12_PORT', FIG_ENV_REGEX)

    def testDoesntMatchWhatDoesntLookLikeFigEnvvar(self):
        self.assertNotRegexpMatches('MONGO_PORT_30', FIG_ENV_REGEX)


class FigvarsTestCase(unittest.TestCase):

    def testWillFilterOnlyWhatLooksLikeFigEnvvar(self):
        allvars = {
            "HOME": "asd", "JAVA_HOME": "", "PATH": "/bin", "container": "lxc",
            "somethingWeird": "", "PORT_3000": "something", "DB_1_PORT": "tcp://172.12.0.2",
            "DB_28_PORT": "tcp://172.12.0.8", "POSTGRES_PORT": "tcp:172.10.1.2",
            "POSTGRES_2_PORT": "tcp://172.12.0.6", "OTHERSERVICE_1_PORT": "tcp://172.12.0.10",
            "OTHERSERVICE_NOTFIG": "whatever..."
        }
        expected = {
            "DB_1_PORT": "tcp://172.12.0.2", "DB_28_PORT": "tcp://172.12.0.8",
            "POSTGRES_2_PORT": "tcp://172.12.0.6", "OTHERSERVICE_1_PORT": "tcp://172.12.0.10"
        }
        self.assertDictEqual(figvars(allvars), expected)


class FigURITestCase(unittest.TestCase):

    def testWillSplitUrlIntoProperChunks(self):
        uri = "tcp://172.17.0.8:5000"
        expected = {
            'uri': 'tcp://172.17.0.8:5000',
            'protocol': 'tcp',
            'host': '172.17.0.8',
            'port': '5000'
        }
        f = FigURI(uri)
        actual = {'uri': f.uri, 'protocol': f.protocol, 'host': f.host, 'port': f.port}
        self.assertDictEqual(actual, expected)

    def testWillRaiseValueErrorIfGivenUnprocessibleURI(self):
        uri = "thisis:/:some::bollocks"
        with self.assertRaises(ValueError):
            FigURI(uri)


class ContainerNameTestCase(unittest.TestCase):

    def testWillSuccessfulyExtractContainerNameFromSingleUnderscoreName(self):
        key = 'DB_12_PORT'
        self.assertEquals('db', container_name(key))

    def testWillSuccessfulyExtractContainerNamesFromMultiUnderscoreName(self):
        key = 'SOME_OTHER_SERVICE_1_PORT'
        self.assertEquals('some_other_service', container_name(key))


class ContainerOrdinalTestCase(unittest.TestCase):

    def testWillReturnOrdinal(self):
        key = 'SOME_SERVICE_13_PORT'
        self.assertEquals(13, container_ordinal(key))


class GroupbyContainersTestCase(unittest.TestCase):

    def testGivenDictKeyedWithFigEnvvarsWillGroupValuesByContainerName(self):
        environ = {
            'DB_1_PORT': "whatever",
            'DB_2_PORT': "whatever",
            'REDIS_3_PORT': "redis...",
        }
        self.assertSetEqual(set(groupby_containers(environ).keys()), {'db', 'redis'})

    def testGroupsWillBeSortedBasingOnKeyNumber(self):
        environ = {
            'DB_1_PORT': "firstdb",
            'DB_2_PORT': "seconddb",
            'REDIS_3_PORT': "secondredis",
            'REDIS_2_PORT': "firstredis",
        }
        grouped = groupby_containers(environ)
        self.assertListEqual(grouped['db'], ["firstdb", "seconddb"])
        self.assertListEqual(grouped['redis'], ["firstredis", "secondredis"])


class ContainersTestCase(unittest.TestCase):

    def testWillMapFigURIOverGivenKwargsAndExtendSelfWithThen(self):
        kwargs = {
            'db': ['tcp://172.12.0.1:5432'],
            'memcached': ['tcp://172.12.0.2:3000', 'tcp://172.12.0.3:3001']
        }
        containers = Containers(**kwargs)
        self.assertEqual(containers.memcached[0].uri, 'tcp://172.12.0.2:3000')
        self.assertEqual(containers.memcached[0].port, '3000')