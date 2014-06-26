import sys, os
import unittest
import traceback
import time
import subprocess

from setuptools import setup

import distutils.core
import distutils.errors
import distutils.dist

import watchdog.events
import watchdog.observers


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


class WatchCommandRunner(watchdog.events.FileSystemEventHandler):
    """
    On any change will execute commands provided to constructor.
    If anyone of them changes will skip following ones and wait for
    changes again.
    """

    def __init__(self, *args):
        self.commands = args
        self.timestamp = time.time()

    def on_any_event(self, event):
        # add a little throttling
        now = time.time()
        if now - self.timestamp < 0.5:
            return
        else:
            self.timestamp = now
        print
        skip = False
        for command in self.commands:
            print "Filesystem change detected..."
            if not skip:
                print "------------------ `{0}` ------------------".format(command)
                retval = subprocess.call(["python", "setup.py", command])
                if retval != 0:
                    print "command `{}` failed. Skipping further commands.".format(command)
                    skip = True
                print "-------------------------------------------"
            else:
                print "skipping `{}`".format(command)
        skip = False
        print
        print "Watching for changes..."


class WatchSource(distutils.core.Command):
    """Watches `src` directory for file changes and runs tests"""
    description = "watch for source changes and run specified commands"
    user_options = [
        ('commands=', 'c', "Whitespace separated list of commands to run on file change")
    ]

    def initialize_options(self):
        self.commands = None

    def finalize_options(self):
        self.commands = self.commands.split()

    def run(self):
        event_handler = WatchCommandRunner(*self.commands)
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, 'src', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


        
setup(
    name = "figgler",
    version = "1.1.1",
    package_dir = {
        '': 'src',
    },
    packages = [
        'figgler',
    ],

    install_requires = [
        'watchdog==0.7.1'
    ],

    author = "Karol Majta",
    author_email = "karolmajta@gmail.com",
    description = "Utilities for reading environment variables in containers instrumented with fig.",
    license = "MIT",
    url = "https://github.com/karolmajta/figgler-python",
    
    cmdclass = {
        'test': RunUnittests,
        'watch': WatchSource
    },
)
