# Flask-Cake

[![Build Status](https://travis-ci.org/rsenk330/Flask-Cake.png?branch=master)](https://travis-ci.org/rsenk330/Flask-Cake)

Support for automatically executing CoffeeScript Cake files for Flask.

## Quickstart

```python
from flask import Flask
from flask_cake import Cake

app = Flask(__name__)
cake = Cake(app)
```

Whenever there is a change in the `static/coffee/` directory, `cake build` is executed.

## More Info

* [Flask-Cake Documentation](http://flask-cake.readthedocs.org/)
* [Cake Documentation](http://coffeescript.org/#cake)
* [Flask Documentation](http://flask.pocoo.org/docs/)
