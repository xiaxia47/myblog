from django.urls import path,re_path
from . import views

app_name = 'article'
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('tag/<int:pk>/',views.TagView.as_view(), name='tag'),
    path('article/<int:article_id>/',views.ArticleDetailView.as_view(),name='detail'),
    path('about/', views.about, name='about'),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:category_id>/',views.CategoryView.as_view(), name='category'),
]

