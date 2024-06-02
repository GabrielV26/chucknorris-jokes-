# jokes/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Joke
import requests
import json

def index(request):
    return render(request, 'index.html')

def get_joke(request):
    category = request.GET.get('category')
    if category:
        url = f'https://api.chucknorris.io/jokes/random?category={category}'
    else:
        url = 'https://api.chucknorris.io/jokes/random'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        joke = data['value']
    else:
        joke = 'Failed to retrieve joke'
    return JsonResponse({'joke': joke})

def add_joke(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            joke_text = data.get('text', '')
            if joke_text:
                Joke.objects.create(text=joke_text)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No joke text provided'}, status=400)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    return HttpResponseBadRequest('Invalid request method or content type')
