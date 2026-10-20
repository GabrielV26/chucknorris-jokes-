# Chuck Norris Jokes

A small Django application that fetches random jokes from the [Chuck Norris API](https://api.chucknorris.io/) and lets users save jokes in a local SQLite database.

## Features

- Fetch a random joke, optionally filtered by category.
- Save a joke through a JSON endpoint.
- Validate incoming data and return meaningful HTTP status codes.
- Apply request timeouts and handle upstream API failures.
- Rate-limit joke retrieval and saving endpoints.
- Limit request body size and enable production security settings.

## Requirements

- Python 3.10 or newer
- pip

## Local setup

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DJANGO_DEBUG=true
python manage.py migrate
python manage.py runserver
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
$env:DJANGO_DEBUG = "true"
python manage.py migrate
python manage.py runserver
```

Local development mode uses a development-only fallback secret. Never use it in deployment.

## Production configuration

Set these environment variables through your hosting provider's secret/configuration manager:

- `DJANGO_SECRET_KEY`: a newly generated, private random secret. The previously committed secret should be considered exposed and rotated.
- `DJANGO_DEBUG=false`
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames, without schemes, e.g. `app.example.com`.
- `DJANGO_SECURE_SSL_REDIRECT=true` (requires HTTPS to be correctly configured at the hosting layer).
- `DJANGO_SECURE_HSTS_SECONDS`: start with a cautious value such as `3600` after confirming HTTPS works.
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true` only if all subdomains support HTTPS.
- `DJANGO_SECURE_HSTS_PRELOAD=true` only after carefully verifying preload requirements.

The application enables secure session and CSRF cookies when `DEBUG=false`. If TLS terminates at a reverse proxy, configure Django's proxy/HTTPS detection according to your hosting provider before enabling redirects; otherwise redirect loops can occur.

Rate limiting uses Django's configured cache. The default local-memory cache is suitable only for development/single-process use; configure a shared cache (such as Redis) in multi-worker or multi-instance deployments so limits are consistent. Also enforce request-size limits at the reverse proxy/web server, because application settings alone cannot protect every server/protocol edge case.

## Endpoints

- `GET /random_joke/` — returns a random joke as JSON. Optional query parameter: `category`. Limited to 30 requests per IP per minute.
- `POST /add_joke/` — saves a joke. Send `Content-Type: application/json` and a body such as `{"text":"A joke"}`. Text must contain 1–2000 characters. Limited to 10 requests per IP per minute.

The save endpoint is protected by Django CSRF middleware; browser requests should include the CSRF token. Rate-limited requests receive HTTP 429. Oversized request bodies receive HTTP 413.

## Checks

```bash
python manage.py test
python manage.py check
python manage.py check --deploy
```

## Tech stack

Python, Django, SQLite, Requests, django-ratelimit, HTML, CSS and JavaScript.
