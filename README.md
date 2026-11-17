# Autoquiz

[![CI](https://github.com/jateeq/Autoquiz/actions/workflows/ci.yml/badge.svg)](https://github.com/jateeq/Autoquiz/actions/workflows/ci.yml)

Autoquiz takes a long piece of text, identifies the concepts a reader needs to understand it,
and generates flashcards from those concepts so the reader can test their recall later.

## Project status

| Part | State |
| --- | --- |
| Web front end (paste text, view results) | Working. Django 5.2 LTS with Bootstrap 5. |
| Key-concept extraction | **Not implemented.** The results page echoes the submitted text. |
| Flashcard generation | Not started. |
| Research | One exploratory notebook that loads a TF-IDF model of English Wikipedia with gensim. |

The front end defines the input and output contract, and the extraction step is the next piece of
work. See [Roadmap](#roadmap).

## How it works

```
browser ──POST text──▶ concierge.views.index ──▶ TargetDocumentForm (validate, ≤200k chars)
                                │
                                ▼
                     [key-concept extraction]   ◀── not yet implemented
                                │
                                ▼
                     concierge/results.html (currently renders the input text)
```

- `src/autoquiz/autoquiz/` contains the Django project (settings, root URLs, WSGI entry point).
- `src/autoquiz/concierge/` contains the Django app that accepts a document and renders results.
- `research/` contains the exploratory notebook. It was written for Python 2 and expects a
  preprocessed Wikipedia corpus (`research/enwiki_processed/`) that is excluded from git because
  of its size. You can build the corpus with gensim's `make_wiki` script from an
  `enwiki-latest-pages-articles.xml.bz2` dump.

## Setup

The project requires Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
export DJANGO_DEBUG=1
uv run python src/autoquiz/manage.py migrate
uv run python src/autoquiz/manage.py runserver
```

Then open http://127.0.0.1:8000/.

### Configuration

The app reads its settings from environment variables.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_DEBUG` | off | Set to `1` for local development. |
| `DJANGO_SECRET_KEY` | none | Required when debug mode is off. The app refuses to start without it. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` in debug mode, empty otherwise | Comma-separated host names. |

## Development

```sh
uv run ruff check .                                      # lint
uv run ruff format .                                     # format
DJANGO_DEBUG=1 uv run python src/autoquiz/manage.py test concierge   # tests
```

CI runs the same commands on Python 3.12 and 3.14 for every pull request.

## Roadmap

1. Define an `extract_concepts(text) -> list[Concept]` interface in a module that has no Django
   dependency, so that it can be developed and tested in isolation.
2. Implement a baseline extractor (for example, TF-IDF or TextRank over noun phrases) and add an
   evaluation fixture with hand-labelled passages.
3. Generate question and answer pairs from the extracted concepts and render them as flashcards.
4. Move long-running extraction off the request thread once input sizes justify it.
