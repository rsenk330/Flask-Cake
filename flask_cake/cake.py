from __future__ import absolute_import

import os
import subprocess

from six import string_types
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
        self.cake_parent = cakeparent

        self._watchdog()

    def _watchdog(self):
        """Runs Watchdog to listen to filesystem events.

        When first run, the `Cakefile` is touched to trigger the
        initial build.

        """
        cake_dir = os.path.abspath(os.path.join(self.app.static_folder, self.cake_parent))

        # Setup Watchdog
        handler = Events(cake_dir=cake_dir, tasks=self.tasks)
        observer = Observer(timeout=5000)
        observer.schedule(handler, path=cake_dir, recursive=True)
        observer.start()

        # "Touch" the Cakefile to signal the initial build
        cakefile = os.path.join(cake_dir, "Cakefile")
        with open(cakefile, 'r'):
            os.utime(cakefile, None)


class Events(FileSystemEventHandler):
    """Handler for all filesystem events."""

    def __init__(self, cake_dir, tasks):
        super(Events, self).__init__()

        self._cake_dir = cake_dir

        # Check to see if the tasks are specified as a single task or multiple
        # tasks.
        if isinstance(tasks, string_types):
            tasks = [tasks]

        self._tasks = tasks

    def on_any_event(self, event):
        nullfh = open(os.devnull, "w")

        # Run `cake build` and send all stdout to `/dev/null`.
        p = subprocess.Popen(["cake"] + self._tasks, cwd=self._cake_dir, stdout=nullfh)
        p.wait()

        nullfh.close()
