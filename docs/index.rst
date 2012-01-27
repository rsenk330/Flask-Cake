.. module:: flask_cake

Flask-Cake
==========

Flask-Cake runs CoffeeScript Cake files automatically on filesystem changes. This is useful, for example, when you want to perform tasks like compile all CoffeeScript files in to JavaScript files.


Installation
------------

The Flask-Cake extension can be easily installed. To install with easy_install:

.. code-block:: sh

    $ easy_install Flask-Cake


Alternatively, if you have pip installed:

.. code-block:: sh

    $ pip install Flask-Cake

Usage
-----

You initialize the extension by creating an instance of :class:`flask_cake.Cake`:

.. code-block:: python

    from flask import Flask
    from flask_cake import Cake

    app = Flask(__name__)
    cake = Cake(app)

Like most Flask extensions, a Flask-Cake instance may be used with multiple applications by initializing with :py:func:`flask_cake.Cake.init_app`:

.. code-block:: python

    app = Flask(__name__)
    cake = Cake()
    cake.init_app(app)

Currently, Flask-Cake requires you to have a directoy structure like this:

.. code-block:: text

    app/
      static/
        coffee/
          Cakefile

Inside the Cakefile, you need to have a ``build`` task. This will be configurable in the future, along with the path to the Cakefile. The ``build`` task can do whatever you want. Here is a simple example that combines many different `.coffee` files into a single `.js` file in a different directory:

.. code-block:: sh

    {exec} = require 'child_process'

    coffeeFiles = [
        'models/users.coffee',
        'controllers/user.coffee',
        'views/user.coffee',
        'login.coffee',
        'app.coffee',
    ]

    task 'build', 'Build PunchedOut! JavaScript file', ->
        console.log 'Building PunchedOut! application.js file...'

        exec "coffee --join app.js --output ../js/ --compile #{coffeeFiles.toString().replace(/,/g, ' ')}"

.. Configuration
.. -------------


CoffeeScript documentation
--------------------------

The following links might be useful for furthur information:

* http://coffeescript.org/
* http://coffeescript.org/#cake
