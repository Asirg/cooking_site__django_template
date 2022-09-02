from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView
import requests

from nyamki.models import Article, ArticleType

# Create your views here.


class IndexView(ListView):
    model=Article
    paginate_by=10
    template_name="user/userprofile.html"

    def get_queryset(self):
        return self.request.user.profile.save_articles.all()

class SaveArticleView(View):
    def post(self, request, id):
        request.user.profile.save_articles.add(id)
        article = Article.objects.get(pk=id)
        return redirect("nyamki:article", slug=article.url)

class DeleteArticleView(View):
    def post(self, request, id):
        request.user.profile.save_articles.remove(id)
        return redirect("user:user", pk=request.user.id)