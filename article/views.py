from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Article
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime
import markdown

# Create your views here.

def index(request):
    article_list = Article.objects.all().order_by('-pub_date')
    return render(request,'article/index.html',context={'post_list':article_list})

def home(request):
    post_list = Article.objects.all()
    paginator = Paginator(post_list,2)
    if 'page'in request.GET:
        page = request.GET['page']
    else:
        page = 1
    try:
        post_cur_page = paginator.page(page)
    except PageNotAnInteger:
        post_cur_page = paginator.page(1)
    except EmptyPage:
        post_cur_page = paginator.paginator(paginator.num_pages)
    return render(request,'article/home.html',{'post_list': post_cur_page})

def detail(request, article_id):
    post = get_object_or_404(Article, pk=article_id)
    post.content = markdown.markdown(post.content, 
                            extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',  #语法高亮
                                'markdown.extensions.toc',       #自动生成目录
                            ])
    return render(request, 'article/detail.html',{'post': post})

def test(request):
    
    post_list = Article.objects.all()
    return render(request,'article/home.html',{'post_list': post_list})

def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    else:
        return render(request,'article/archives.html',
                      {'post_list': post_list,'error': False}) 

def search(request,category=None):
    result = {'error':False,'msg':None}
    if 'keyword'in request.GET:
        keyword = request.GET['keyword']
        post_list = Article.objects.filter(title__contains=keyword)
    else:
        post_list = Article.objects.filter(category=category)
    if len(post_list) == 0:
       result['msg'] = "未查询到相关内容"
       result['error'] = True
    return render(request, 'article/search.html',
                  {'post_list': post_list,'result': result})



def about(request):
    return render(request,'article/aboutme.html')
