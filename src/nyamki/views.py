from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView

from nyamki.models import Category, Label, Keyword, Article, GroupOfIngredients, Ingredient, Unit, CookingIngredient, GroupOfInstructions, Instruction, Comment

# Create your views here.

class IndexView(ListView):
    model=Article
    template_name="nyamki/index.html"


class ArticleListView(ListView):
    model=Article

    paginate_by = 10

    template_name = "nyamki/article_category.html"

    def get(self, request, *args, **kwargs):
        self.object_list = Article.objects.filter(**{f"{kwargs['type']}__url":kwargs['value']}, draft=False)
        context = super().get_context_data()

        if kwargs['type'] == "categories":
            context["category"] = Category.objects.filter(url=kwargs['value']).first()

        return super().render_to_response(context)

class ArticleView(DetailView):
    model = Article
    slug_field = "url"

    template_name = "nyamki/article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comment_set.order_by('date')
        context['dishes_bar'] = Article.objects.order_by('?')[:10]
        return context

class SearchView(ListView):
    model=Article

    paginate_by = 10

    template_name="nyamki/search.html"

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            queryset = Article.objects.filter(name__icontains=q.lower())
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

    def get_queryset(self):
        return Article.objects.filter(name__isnull=False, type_id=1)

class ArticlePrintView(DetailView):
    model = Article
    slug_field = "url"

    template_name = "nyamki/article_print.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
