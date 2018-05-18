from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=10, blank=False, default='日志') #博客分类
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10,blank=False, default='技术') #文章标签
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100) #博客题目
    author = models.CharField(max_length=30,default='匿名') #作者
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT,default='默认分类') #分类
    tag = models.ManyToManyField(Tag, blank=True) # 标签
    pub_date = models.DateTimeField(auto_now_add=True) #博客日期
    modyfied_date = models.DateTimeField(auto_now=True) #最近一次修改时间
    excerpt = models.CharField(max_length=200, blank=True) # 摘要
    content = models.TextField(blank=True) #文章正文

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail',kwargs={'article_id' : self.pk})

    class Meta:
        ordering = ['-pub_date']

