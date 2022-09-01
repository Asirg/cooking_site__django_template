from django import template

from nyamki.models import Article, Category, Label, Keyword

register = template.Library()

@register.simple_tag()
def get_recipe_categories():
    return Category.objects.filter(for_article=0)

@register.simple_tag()
def get_recipe_labels():
    return Label.objects.all()

@register.simple_tag()
def get_recipe_keywords():
    return Keyword.objects.all()

@register.simple_tag()
def get_article_category():
    return Category.objects.filter(for_article=1)

@register.simple_tag()
def get_articles_list(type, count):
    queryset = Article.objects.filter(type__name_ru=type, name__isnull=False).order_by("date")[:count]
    return queryset

@register.filter()
def get_item(value, key):
    return value[key]