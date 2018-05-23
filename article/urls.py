from django.urls import path,re_path
from . import views

app_name = 'article'
urlpatterns = [
    path('',views.index,name='index'),
    path('article/<int:article_id>/',views.detail,name='detail'),
    path('about/', views.about, name='about'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('category/<int:category_id>/',views.category, name='category'),
]

