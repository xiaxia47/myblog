from django.urls import path,re_path
from . import views

app_name = 'article'
urlpatterns = [
    path('',views.index,name='index'),
    path('article/<int:article_id>',views.detail,name='detail'),
    path('test/',views.test, name='test'),
    path('about/', views.about, name='about'),
    path('archives/', views.archives, name='archives'),
    path('search/<str:category>/',views.search, name='search'),
    re_path(r'^search/',views.search, name='search'),
]

