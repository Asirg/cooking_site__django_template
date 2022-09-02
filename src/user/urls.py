from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path('<int:pk>', views.IndexView.as_view(), name="user"),
    path('save_article/<int:id>', views.SaveArticleView.as_view(), name="save_article"),
    path('delete_article/<int:id>', views.DeleteArticleView.as_view(), name="delete_article"),
]