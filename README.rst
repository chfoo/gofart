GoFart
======

GoFart is a URL fartener. It provides a URL fartening service.


Quick Start
===========

You will need

* Python 3
* Tornado web

Once you install Python, install the dependencies::

    pip3 install tornado

Then start up GoFart behind a web server (such as Nginx)::

    python3 -m gofart --host localhost --port 8000 --xheaders

Then access a URL like ``http://yourservice.xample/https/google.com/``.
