import pytest

try:
    from unittest import mock  # Python 3
except ImportError:
    import mock


@pytest.fixture
def app(tmpdir):
    from flask import Flask

    root_path = tmpdir.ensure("test-proj", dir=True)

    tmpdir.ensure("test-proj/static/coffee", dir=True)
    p = tmpdir.join("test-proj/static/coffee", "Cakefile")
    p.write("")

    app = Flask(__name__)
    app.root_path = root_path.strpath
    return app


def test_cake_init(app):
    from flask_cake import Cake

    cake = Cake(app)
    assert cake.app == app
    assert cake.tasks == ["build"]
    assert cake.cake_parent == "coffee"


def test_watchdog(app, tmpdir):
    from flask_cake import Cake

    with mock.patch("watchdog.observers.Observer.schedule") as mock_schedule:
        Cake(app)

        cake_dir = tmpdir.join("test-proj/static/coffee").strpath
        mock_schedule.assert_called_once_with(mock.ANY, path=cake_dir, recursive=True)


def test_events_on_any_event(app):
    from flask_cake.cake import Events
    e = Events(app.root_path, tasks=["build"])

    with mock.patch("flask_cake.cake.subprocess") as subprocess:
        e.on_any_event(None)
        subprocess.Popen.assert_called_once_with(["cake", "build"], cwd=app.root_path, stdout=mock.ANY)


def test_events_on_any_event_str(app):
    from flask_cake.cake import Events
    e = Events(app.root_path, tasks="build")

    with mock.patch("flask_cake.cake.subprocess") as subprocess:
        e.on_any_event(None)
        subprocess.Popen.assert_called_once_with(["cake", "build"], cwd=app.root_path, stdout=mock.ANY)
