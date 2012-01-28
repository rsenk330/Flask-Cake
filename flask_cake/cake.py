from __future__ import absolute_import

import os
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Cake(object):
    def __init__(self, app=None, tasks=["build"], cakeparent="coffee"):
        """Initalize a new instance of Flask-Cake.

        :param app: The Flask app
        :param tasks: A string containing a cake "task" to execute or a list
                      of multiple cake tasks to run. By default, this will run
                      ``cake build``.
        :param str cakeparent: The directory where the Cakefile is located
                               relative to Flask's `static_path`. By default,
                               this is `coffee/`, meaning that the Cakefile is
                               located at `static_path/coffee/Cakefile`.

        """
        self.init_app(app, tasks, cakeparent)

    def init_app(self, app, tasks=["build"], cakeparent="coffee"):
        """Initalize a new instance of Flask-Cake.

        :param app: The Flask app
        :param tasks: A string containing a cake "task" to execute or a list
                      of multiple cake tasks to run. By default, this will run
                      ``cake build``.
        :param str cakeparent: The directory where the Cakefile is located
                               relative to Flask's `static_path`. By default,
                               this is `coffee/`, meaning that the Cakefile is
                               located at `static_path/coffee/Cakefile`.

        """
        self.app = app
        self.tasks = tasks
        self.cakeparent = cakeparent

        self._watchdog()

    def _watchdog(self):
        """Runs Watchdog to listen to filesystem events.

        When first run, the `Cakefile` is touched to trigger the
        initial build.

        """
        if not hasattr(self.app, 'static_url_path'):
            from warnings import warn
            warn(
                DeprecationWarning('static_path is called static_url_path since Flask 0.7'),
                stacklevel=2
            )

            static_url_path = self.app.static_path
        else:
            static_url_path = self.app.static_url_path

        static_dir = self.app.root_path + static_url_path

        cakedir = os.path.join(static_dir, self.cakeparent)

        # Setup Watchdog
        handler = Events(cakedir=cakedir, tasks=self.tasks)
        observer = Observer(timeout=5000)
        observer.schedule(handler, path=cakedir, recursive=True)
        observer.start()

        # "Touch" the Cakefile to signal the initial build
        cakefile = os.path.join(cakedir, "Cakefile")
        with file(cakefile, 'a'):
            os.utime(cakefile, None)

class Events(FileSystemEventHandler):
    """Handler for all filesystem events."""

    def __init__(self, cakedir, tasks):
        super(Events, self).__init__()

        self._cakedir = cakedir
        self._tasks = tasks

    def on_any_event(self, event):
        nullfh = open(os.devnull, "w")

        # Check to see if the tasks are specified as a single task or multiple
        # tasks.
        if isinstance(self._tasks, basestring):
            tasks = [self._tasks]
        else:
            tasks = self._tasks

        # Run `cake build` and send all stdout to `/dev/null`.
        p = subprocess.Popen(["cake"] + tasks, cwd=self._cakedir, stdout=nullfh)
        p.wait()

        nullfh.close()
