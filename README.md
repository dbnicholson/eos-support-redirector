# eos-support-redirector

A simple python [WSGI][wsgi] webapp for redirecting from old Endless
support URLs on Zendesk to the new Endless support site.

[wsgi]: https://wsgi.readthedocs.io/en/latest/index.html

## Running

Any WSGI server will work. For example, using [gunicorn][gunicorn]:

```
gunicorn redirector:application
```

[gunicorn]: https://gunicorn.org/

## Configuration

There is no configuration except for the base URL used for redirects. By
default this is https://support.endlessos.org, but this can be changed
via the `SUPPORT_URL` environment variable.
