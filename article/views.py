from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Article,Category
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime
from comment.forms import CommentForm
from django.views.generic import ListView, DetailView
import markdown

# Create your views here.

class IndexView(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'

    paginate_by = 5

class CategoryView(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(pub_date__year=year,
                                                               pub_date__month=month)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/detail.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    
    def get_object(self, queryset=None):
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        article.content = markdown.markdown(article.content, 
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({ 'form': form,
                         'comment_list': comment_list,
        })
        return context



def about(request):
    return render(request,'article/aboutme.html')

