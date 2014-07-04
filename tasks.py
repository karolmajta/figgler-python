import os, sys, time
import unittest.runner

from invoke import run, task
from invoke.exceptions import Failure

import watchdog.events, watchdog.observers

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'src'))


@task(name='unittest')
def unit():
    loader = unittest.TestLoader()
    tests = loader.discover('src/tests')
    testRunner = unittest.runner.TextTestRunner()
    result = testRunner.run(tests)
    if len(result.errors) > 0 or len(result.failures) > 0:
        tpl = "Test runner reported {0} failures and {1} errors."
        msg = tpl.format(len(result.failures), len(result.errors))
        raise Failure(result)


@task
def watch():
    event_handler = Watcher('invoke unittest')
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, 'src', recursive=True)
    observer.start()
    print "\t [WATCHER] started watcher..."
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class Watcher(watchdog.events.FileSystemEventHandler):
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
            print "\t [WATCHER] Filesystem change detected..."
            print
            if not skip:
                result = run(command)
                skip = result.exited != 0
            else:
                print "\t [WATCHER] skipping `{}`".format(command)
        skip = False
        print
        print "\t [WATCHER] Watching for changes..."