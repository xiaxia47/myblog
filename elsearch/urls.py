#_*_ coding:utf-8 _*_
import django.urls import path
from . import views

app_name='elsearch'
urlpatterns = [
    path('elsearch/',views.SearchView.as_view(),name='search'),
    path('suggest/',views.SearchSuggest.as_view(),name='suggest'),
    path('simplesearch/'), views.IndexView.as_view(), name='index'),
]




