from django.urls import path

from nyamki import views

app_name = "nyamki"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('calculator/', views.СalculatorView.as_view(), name="calculator"),
    path('comment/<int:user_pk>/<int:article_pk>', views.AddComment.as_view(), name="addcomment"),
    path('filter/<str:type>/<str:value>', views.ArticleListView.as_view(), name="filter"),
    path('article/<str:slug>', views.ArticleView.as_view(), name="article"),
    path('article/print/<str:slug>', views.ArticlePrintView.as_view(), name="print"),
]