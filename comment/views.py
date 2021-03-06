from django.shortcuts import render, get_object_or_404, redirect
from article.models import Article

from .forms import CommentForm


# Create your views here.
def post_comment(request, article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect(article)
        else:
            comment_list = post.comment_set.all()
            context = {'post':post,'form': form,
                       'comment_list': comment_list
                      }
            return render(request,'article/Article',
                          context=context)
    return redirect(post)

