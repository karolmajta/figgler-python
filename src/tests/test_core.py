import unittest

from figgler.core import FIG_ENV_REGEX, figvars, FigURI, container_name, groupby_containers, \
    split_uri, squash_ports, container_ordinal, Containers


class FigenvRegexTestCase(unittest.TestCase):

    def testDoesMatchEnvvarWithPortChunk(self):
        self.assertRegexpMatches('DB_1_PORT_8000_TCP', FIG_ENV_REGEX)

    def testDoesntMatchEnvvarWithoutPortChunk(self):
        self.assertNotRegexpMatches('DB_2_PORT', FIG_ENV_REGEX)

    def testMatchesNthInstance(self):
        self.assertRegexpMatches('DB_28_PORT_5000_TCP', FIG_ENV_REGEX)

    def testMatchesNamesWithUnerscores(self):
        self.assertRegexpMatches('MONGO_DB_12_PORT_27001_TCP', FIG_ENV_REGEX)

    def testDoesntMatchWhatDoesntLookLikeFigEnvvar(self):
        self.assertNotRegexpMatches('MONGO_PORT_30', FIG_ENV_REGEX)


class FigvarsTestCase(unittest.TestCase):

    def testWillFilterOnlyWhatLooksLikeFigEnvvar(self):
        allvars = {
            "HOME": "asd", "JAVA_HOME": "", "PATH": "/bin", "container": "lxc",
            "somethingWeird": "", "PORT_3000": "something", "DB_1_PORT_43000_TCP": "tcp://172.12.0.2",
            "DB_28_PORT_28_TCP": "tcp://172.12.0.8", "POSTGRES_PORT": "tcp:172.10.1.2",
            "POSTGRES_2_PORT_5432_TCP": "tcp://172.12.0.6", "OTHERSERVICE_NOTFIG": "whatever..."
        }
        expected = {
            "DB_1_PORT_43000_TCP": "tcp://172.12.0.2", "DB_28_PORT_28_TCP": "tcp://172.12.0.8",
            "POSTGRES_2_PORT_5432_TCP": "tcp://172.12.0.6"
        }
        self.assertDictEqual(figvars(allvars), expected)


class splitUriTestCase(unittest.TestCase):

    def testWillSplitUrlIntoProperChunks(self):
        uri = "tcp://172.17.0.8:5000"
        expected = {
            'protocol': 'tcp',
            'host': '172.17.0.8',
            'port': '5000'
        }
        self.assertDictEqual(split_uri(uri), expected)

    def testWillRaiseValueErrorIfGivenUnprocessibleURI(self):
        uri = "thisis:/:some::bollocks"
        with self.assertRaises(ValueError):
            split_uri(uri)


class squashPortsTestCase(unittest.TestCase):

    def testWillSquashIntoOneDictsBasingOnPortKey(self):
        containers = [
            {'port': 90, 'host': '172.2.0.1', 'protocol': 'tcp'},
            {'port': 91, 'host': '172.2.0.1', 'protocol': 'tcp'}
        ]
        expected = [{'ports': [90, 91], 'host': '172.2.0.1', 'protocol': 'tcp'}]
        self.assertListEqual(expected[0]['ports'], squash_ports(containers)[0]['ports'])


class FigURITestCase(unittest.TestCase):

    pass


class ContainerNameTestCase(unittest.TestCase):

    def testWillSuccessfulyExtractContainerNameFromSingleUnderscoreName(self):
        key = 'DB_12_PORT_5000_TCP'
        self.assertEquals('db', container_name(key))

    def testWillSuccessfulyExtractContainerNamesFromMultiUnderscoreName(self):
        key = 'SOME_OTHER_SERVICE_1_PORT_3000_TCP'
        self.assertEquals('some_other_service', container_name(key))


class ContainerOrdinalTestCase(unittest.TestCase):

    def testWillReturnOrdinal(self):
        key = 'SOME_SERVICE_13_PORT_3000_TCP'
        self.assertEquals(13, container_ordinal(key))


class GroupbyContainersTestCase(unittest.TestCase):

    def testGivenDictKeyedWithFigEnvvarsWillGroupValuesByContainerName(self):
        environ = {
            'DB_1_PORT_80_TCP': 'tcp://172.2.0.1:5000',
            'DB_2_PORT_90_TCP': 'tcp://172.2.0.1:5001',
            'REDIS_3_PORT_30_TCP': 'tcp://172.2.0.1:5002',
        }
        self.assertSetEqual(set(groupby_containers(environ).keys()), {'db', 'redis'})

    def testPortsWillBeMergedIntoListsAndSortedAscending(self):
        environ = {
            'DB_1_PORT_5000_TCP': "tcp://172.0.2.1:5000",
            'DB_1_PORT_6000_TCP': "tcp://172.0.2.1:6000",
            'HTTP_1_PORT_80_TCP': "tcp://172.0.2.3:80",
            'HTTP_2_PORT_80_TCP': "tcp://172.0.2.4:80",
        }
        grouped = groupby_containers(environ)
        self.assertListEqual(grouped['db'][0]['ports'], ['5000', '6000'])
        self.assertListEqual(grouped['http'][0]['ports'], ['80'])
        self.assertListEqual(grouped['http'][1]['ports'], ['80'])


class ContainersTestCase(unittest.TestCase):

    def testWillMapFigURIOverGivenKwargsAndExtendSelfWithThen(self):
        kwargs = {
            'db': [
                {'protocol': 'tcp', 'host': '172.12.0.1', 'ports': ['5432']}
            ],
            'memcached': [
                {'protocol': 'tcp', 'host': '172.12.0.2', 'ports': ['3001', '3000']},
                {'protocol': 'tcp', 'host': '172.12.0.3', 'ports': ['3001', '3000']}
            ]
        }
        containers = Containers(**kwargs)
        self.assertListEqual(containers.memcached[0].ports, ['3000', '3001'])
