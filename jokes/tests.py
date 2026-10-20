import json
from unittest.mock import Mock, patch

import requests
from django.test import TestCase
from django.urls import reverse

from .models import Joke


class GetJokeTests(TestCase):
    @patch("jokes.views.requests.get")
    def test_returns_random_joke(self, mock_get):
        response_mock = Mock()
        response_mock.json.return_value = {"value": "A funny joke"}
        response_mock.raise_for_status.return_value = None
        mock_get.return_value = response_mock

        response = self.client.get(reverse("random_joke"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"joke": "A funny joke"})
        self.assertEqual(mock_get.call_args.kwargs["timeout"], (3.05, 10))

    @patch("jokes.views.requests.get")
    def test_passes_category_as_parameter(self, mock_get):
        response_mock = Mock()
        response_mock.json.return_value = {"value": "A category joke"}
        response_mock.raise_for_status.return_value = None
        mock_get.return_value = response_mock

        response = self.client.get(reverse("random_joke"), {"category": "animal"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_get.call_args.kwargs["params"], {"category": "animal"})

    def test_rejects_invalid_category(self):
        response = self.client.get(reverse("random_joke"), {"category": "animal&x=1"})
        self.assertEqual(response.status_code, 400)

    @patch("jokes.views.requests.get", side_effect=requests.Timeout)
    def test_handles_api_timeout(self, _mock_get):
        response = self.client.get(reverse("random_joke"))
        self.assertEqual(response.status_code, 502)

    @patch("jokes.views.requests.get")
    def test_handles_malformed_api_response(self, mock_get):
        response_mock = Mock()
        response_mock.json.return_value = {}
        response_mock.raise_for_status.return_value = None
        mock_get.return_value = response_mock

        response = self.client.get(reverse("random_joke"))
        self.assertEqual(response.status_code, 502)

    def test_rejects_non_get_method(self):
        response = self.client.post(reverse("random_joke"))
        self.assertEqual(response.status_code, 405)


class AddJokeTests(TestCase):
    def post_json(self, payload):
        return self.client.post(
            reverse("add_joke"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_saves_trimmed_joke(self):
        response = self.post_json({"text": "  A saved joke  "})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Joke.objects.get().text, "A saved joke")

    def test_rejects_invalid_json(self):
        response = self.client.post(
            reverse("add_joke"), data="{invalid", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Joke.objects.count(), 0)

    def test_rejects_non_string_text(self):
        response = self.post_json({"text": 123})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Joke.objects.count(), 0)

    def test_rejects_empty_text(self):
        response = self.post_json({"text": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Joke.objects.count(), 0)

    def test_rejects_text_over_limit(self):
        response = self.post_json({"text": "x" * 2001})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Joke.objects.count(), 0)

    def test_rejects_wrong_content_type(self):
        response = self.client.post(reverse("add_joke"), data="text=hello")
        self.assertEqual(response.status_code, 415)

    def test_rejects_non_post_method(self):
        response = self.client.get(reverse("add_joke"))
        self.assertEqual(response.status_code, 405)
