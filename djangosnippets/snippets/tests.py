from django.contrib.auth.backends import UserModel
from djangosnippets.settings import TEMPLATES
from django.http import HttpRequest, request, response
from django.test import TestCase
from .views import top, snippet_new, snippet_edit, snippet_detail
from django.urls import resolve
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from snippets.models import Snippet
from snippets.views import top

UserModel = get_user_model()

class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expectedtitle(self):
        response = self.client.get("/")
        self.assertContains(response, "Djangoスニペット", status_code=200)
    
    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "snippets/top.html")

class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(username="test_user", 
        email="test@example.com", password="top_secret_pass0001")

        self.snippet = Snippet.objects.create(
            title = "title1",
            code = "print('hello')",
            description = "description1",
            created_by = self.user
        )

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)
    
    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)