# AGENTS.md

This file gives coding agents and new contributors the context they need to work in this
repository. Read [README.md](README.md) first for the product description and project status.

## Repository layout

| Path | Contents |
| --- | --- |
| `pyproject.toml`, `uv.lock` | Dependencies and tool configuration. uv manages the environment. |
| `src/autoquiz/manage.py` | Django management entry point. |
| `src/autoquiz/autoquiz/` | Django project package: `settings.py`, root `urls.py`, `wsgi.py`. |
| `src/autoquiz/concierge/` | The only Django app. It owns the forms, views, templates, and tests. |
| `src/autoquiz/concierge/tests/` | Django `TestCase` suites. |
| `research/` | Exploratory notebooks (Python 2, gensim). They are excluded from linting and CI. |
| `.github/workflows/ci.yml` | Lint, Django system checks, migration check, and tests. |

## Commands

Run every command from the repository root.

```sh
uv sync                                                    # install dependencies
export DJANGO_DEBUG=1                                      # required locally; see below
uv run python src/autoquiz/manage.py runserver             # dev server on :8000
uv run python src/autoquiz/manage.py test concierge        # tests
uv run ruff check . && uv run ruff format --check .        # lint and format check
uv run python src/autoquiz/manage.py makemigrations --check --dry-run
```

`settings.py` raises `ImproperlyConfigured` at import time when `DJANGO_DEBUG` is off and
`DJANGO_SECRET_KEY` is unset. Set one of the two before running any `manage.py` command.

## Conventions

- Target Django 5.2 LTS APIs. Use `django.urls.path`, because `django.conf.urls.url` was removed in
  Django 4.0. Use namespaced URL names (`{% url 'concierge:index' %}`) and never hard-code paths.
- Templates extend `concierge/base.html` and override `{% block content %}`, plus
  `{% block title %}` when the page needs its own title.
- Bootstrap 5.3 is loaded from jsDelivr with Subresource Integrity hashes. When you bump the
  version, recompute both hashes:
  `curl -sL <url> | openssl dgst -sha384 -binary | openssl base64 -A`.
- Read configuration from environment variables in `settings.py` and never commit secrets.
- Use the module-level `logging.getLogger(__name__)` for logging. Do not log submitted document
  text, because users may paste private material.
- Every view change needs a test in `concierge/tests/`. Cover the invalid-input path as well as
  the success path.
- Ruff configuration is in `pyproject.toml`. CI fails on lint or formatting errors.

## Current state and planned work

- `concierge.views.index` validates input and renders `results.html` with the raw text. The
  key-concept extraction step does not exist yet.
- Implement extraction as a plain Python module (for example `src/autoquiz/extraction/`) that does
  not import Django, and call it from the view. Keep the view responsible only for HTTP concerns.
- The app has no models. If you add models, commit their migrations, because CI runs
  `makemigrations --check`.

## Pull requests

- Keep each pull request focused on one change and describe how you verified it.
- Run the tests, the lint, and the format check locally before you push.
