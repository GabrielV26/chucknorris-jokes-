# Chuck Norris Jokes

A small Django application that fetches random jokes from the [Chuck Norris API](https://api.chucknorris.io/) and lets users save jokes in a local SQLite database.

## Features

- Fetch a random joke, optionally filtered by category.
- Save a joke through a JSON endpoint.
- Validate incoming data and return meaningful HTTP status codes.
- Apply request timeouts and handle upstream API failures.

## Requirements

- Python 3.10 or newer
- pip

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

Set `DJANGO_SECRET_KEY` to a private random value before deployment. Configure `DJANGO_DEBUG=false` and `DJANGO_ALLOWED_HOSTS` as a comma-separated list of allowed hostnames in deployed environments. Never commit secrets to Git.

## Endpoints

- `GET /` — application interface.
- `GET /random_joke/` — returns a random joke as JSON. Optional query parameter: `category`.
- `POST /add_joke/` — saves a joke. Send `Content-Type: application/json` and a body such as `{"text":"A joke" }`. Text must contain 1–2000 characters.

The save endpoint is protected by Django CSRF middleware; browser requests should include the CSRF token.

## Checks

```bash
python manage.py test
python manage.py check
```

## Tech stack

Python, Django, SQLite, Requests, HTML, CSS and JavaScript.
