from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Article,Category,Tag
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from comment.forms import CommentForm
from django.views.generic import ListView, DetailView
import markdown

# Create your views here.

class PagingView(ListView):
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context
 
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
           return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right [-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number -3) if (page_number -3)> 0 else 0:page_number -1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number -3 ) > 0 else 0: page_number -1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right [-1] < total_pages:
                last = True
            if left[0] >2:
               left_has_more = True
            if left[0] >1:
               first = True

        data = {'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last':last}
        return data


class IndexView(PagingView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'
    

class CategoryView(PagingView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(PagingView):
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


class TagView(PagingView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag)


def about(request):
    return render(request,'article/aboutme.html')

