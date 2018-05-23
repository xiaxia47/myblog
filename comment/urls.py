from django.urls import path, re_path

from . import views

app_name = 'comment'
urlpatterns = [
    path('comment/article/<int:article_pk>/', views.post_comment, name='post_comment'),
]
