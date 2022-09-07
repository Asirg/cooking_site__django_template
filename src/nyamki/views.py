from shutil import register_unpack_format
from unicodedata import category
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView

from django.core import serializers

from nyamki.models import Category, Label, Keyword, Article, GroupOfIngredients, Ingredient, Unit, CookingIngredient, GroupOfInstructions, Instruction, Comment

import json


# Create your views here.

class IndexView(ListView):
    model=Article
    template_name="nyamki/index.html"


class ArticleListView(ListView):
    model=Article

    paginate_by = 10

    template_name = "nyamki/article_category.html"

    def get_queryset(self):
        if self.kwargs['type'] == "user":
            return self.request.user.profile.save_articles.all().filter(type_id=1)
        return Article.objects.filter(**{f"{self.kwargs['type']}__url":self.kwargs['value']}, draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['type'] == "categories":
            context["category"] = Category.objects.filter(url=self.kwargs['value']).first()
        return context

    def get(self, request, *args, **kwargs):
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            queryset = list(self.get_queryset().filter(type_id=1).values("url", "name", "image"))
            return JsonResponse(queryset, safe=False)

        return super().get(request, *args, **kwargs)

class ArticleView(DetailView):
    model = Article
    slug_field = "url"

    template_name = "nyamki/article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comment_set.order_by('date')
        context['nutritional_value'] = self.get_object().get_nutritional_value()

        context['dishes_bar'] = Article.objects.order_by('?')[:10]
        return context

    def get(self, request, *args, **kwargs):
    
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            obj = self.get_object()
            recipe_data = {
                **obj.get_nutritional_value(),
                **obj.get_ingredients()
            }
            return JsonResponse(recipe_data, safe=False)

        return super().get(request, *args, **kwargs)

class SearchView(ListView):
    model=Article

    paginate_by = 10

    template_name="nyamki/search.html"

    def get(self, request, *args, **kwargs):

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            q = self.request.GET.get("q")
            if q:
                queryset = list(Article.objects.filter(name__icontains=q.lower(), type_id=1, draft=False).values("url", "name", "image"))
                return JsonResponse(queryset, safe=False)
            else:
                return JsonResponse({})

        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            queryset = Article.objects.filter(name__icontains=q.lower(), draft=False)
        else:
            queryset = super().get_queryset()
        return queryset

class AddComment(View):
    """Добавления комментария"""

    def post(self, request, user_pk, article_pk):

        user = get_user_model().objects.get(id=user_pk)
        article = Article.objects.get(id=article_pk)
        
        id = request.POST.get("parent")
        id = int(id) if id else False
        if id > 0 or not id:
            parent = Comment.objects.get(pk=id) if id else None

            comment = Comment(
                user=user,
                article=article,
                parent=parent,
                content=request.POST.get("content")
            )
        else:
            comment = Comment.objects.get(pk=-id)
            comment.content = request.POST.get('content')

        comment.save()
    
        return redirect(reverse("nyamki:article", args=(article.url, )))

class СalculatorView(ListView):
    model=Article

    template_name="nyamki/calculator.html"

    def get_queryset(self):
        return self.request.user.profile.save_articles.all().filter(type_id=1)

class ArticlePrintView(DetailView):
    model = Article
    slug_field = "url"

    template_name = "nyamki/article_print.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
