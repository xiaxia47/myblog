from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

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
    views = models.PositiveIntegerField(default=0) #浏览数

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail',kwargs={'article_id' : self.pk})

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
               'markdown.extensions.extra',
               'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Article,self).save(*args, **kwargs)
    
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-pub_date']

