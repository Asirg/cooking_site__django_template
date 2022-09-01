from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView
import requests

from nyamki.models import Article
import user

# Create your views here.


class IndexView(TemplateView):
    template_name="user/userprofile.html"

class SaveArticleView(View):
    def post(self, request, id):
        request.user.profile.save_articles.add(id)
        article = Article.objects.get(pk=id)
        return redirect("nyamki:article", slug=article.url)