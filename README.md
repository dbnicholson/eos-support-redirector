# eos-support-redirector

A simple python [WSGI][wsgi] webapp for redirecting from old Endless
support URLs on Zendesk to the new Endless support site.

[wsgi]: https://wsgi.readthedocs.io/en/latest/index.html

## Running

Any WSGI server will work. For example, using [gunicorn][gunicorn]:

```
gunicorn redirector:application
```

A [Docker][docker] image with `gunicorn` can also be used. First, build
the image:

```
docker build -t redirector .
```

Then start the container with port 8000 published:

```
docker run -p 8000:8000 redirector
```

[gunicorn]: https://gunicorn.org/
[docker]: https://www.docker.com/

## Configuration

There is no configuration except for the base URL used for redirects. By
default this is https://support.endlessos.org, but this can be changed
via the `SUPPORT_URL` environment variable.

## Testing

Tests can be run from the `test.py` script. This uses python's
[unittest][unittest] framework from the standard library.

[unittest]: https://docs.python.org/3/library/unittest.html
