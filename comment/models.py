from django.db import models
from django.forms import ModelForm

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='昵称',default='游客')
    email = models.EmailField(max_length=100, verbose_name='电子邮箱')
    url = models.URLField(blank=True, verbose_name='个人门户')
    text = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    article = models.ForeignKey('article.Article',on_delete=models.CASCADE)
   
    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering= ['-created_time']

