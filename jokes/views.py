import json
import re

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import Joke

CHUCK_NORRIS_API_URL = "https://api.chucknorris.io/jokes/random"
CATEGORY_PATTERN = re.compile(r"^[a-z0-9_-]{1,50}$")
MAX_JOKE_LENGTH = 2000


def index(request):
    return render(request, "index.html")


@require_GET
def get_joke(request):
    category = (request.GET.get("category") or "").strip()
    if category and not CATEGORY_PATTERN.fullmatch(category):
        return JsonResponse({"error": "Invalid category."}, status=400)

    params = {"category": category} if category else None
    try:
        response = requests.get(CHUCK_NORRIS_API_URL, params=params, timeout=(3.05, 10))
        response.raise_for_status()
        data = response.json()
        joke = data.get("value") if isinstance(data, dict) else None
        if not isinstance(joke, str) or not joke.strip():
            raise ValueError("The API response does not contain a valid joke.")
    except (requests.RequestException, ValueError):
        return JsonResponse(
            {"error": "Could not retrieve a joke right now. Please try again."},
            status=502,
        )
    return JsonResponse({"joke": joke})


@require_POST
def add_joke(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"status": "error", "message": "Content-Type must be application/json."},
            status=415,
        )
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)

    if not isinstance(data, dict):
        return JsonResponse(
            {"status": "error", "message": "JSON body must be an object."}, status=400
        )
    joke_text = data.get("text")
    if not isinstance(joke_text, str):
        return JsonResponse(
            {"status": "error", "message": "The 'text' field must be a string."},
            status=400,
        )
    joke_text = joke_text.strip()
    if not joke_text:
        return JsonResponse(
            {"status": "error", "message": "Joke text cannot be empty."}, status=400
        )
    if len(joke_text) > MAX_JOKE_LENGTH:
        return JsonResponse(
            {"status": "error", "message": f"Joke text cannot exceed {MAX_JOKE_LENGTH} characters."},
            status=400,
        )
    Joke.objects.create(text=joke_text)
    return JsonResponse({"status": "success"}, status=201)
