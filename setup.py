import sys, os
import unittest
import traceback
import time
import subprocess

from setuptools import setup

import distutils.core
import distutils.errors
import distutils.dist


class FailedTestsError(distutils.errors.DistutilsError):
    """One or more tests failed"""


class RunUnittests(distutils.core.Command):
    """Custom test command"""
    description = "run unit tests"
    user_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        # make sure robust_urls is on sys.path. If it is present do nothing,
        # we shall run tests on the present instance. If it's not present
        # add `src` to python path (this means we are testing a source checkout)
        try:
            import figgler
        except ImportError:
            project_root = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(os.path.join(project_root, 'src'))

        loader = unittest.TestLoader()
        tests = loader.discover('src/tests')
        testRunner = unittest.runner.TextTestRunner()
        result = testRunner.run(tests)
        if len(result.errors) > 0 or len(result.failures) > 0:
            tpl = "Test runner reported {0} failures and {1} errors."
            msg = tpl.format(len(result.failures), len(result.errors))
            raise FailedTestsError(msg)

 
setup(
    name = "figgler",
    version = "1.1.2",
    package_dir = {
        '': 'src',
    },
    packages = [
        'figgler',
    ],

    install_requires = [],

    author = "Karol Majta",
    author_email = "karolmajta@gmail.com",
    description = "Utilities for reading environment variables in containers instrumented with fig.",
    license = "MIT",
    url = "https://github.com/karolmajta/figgler-python",
    
    cmdclass = {
        'test': RunUnittests,
    },
)
