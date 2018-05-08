from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=10, blank=False) #博客分类


class Tag(models.Model):
    name = models.CharField(max_length=10,blank=False) #文章标签
~

class Article(models.Model):
    title = models.CharField(max_length=100) #博客题目
    category = models.ForeignKey(Category) #分类
    tag = models.ManytoManyField(Tag, blank=True) # 标签
    pub_date = models.DateTimeField(auto_now_add=True) #博客日期
    modyfied_date = models.DateTimeField(auto_now=True) #最近一次修改时间
    excerpt = models.CharField(max_length=200, blank=True) # 摘要
    content = models.TextField(blank=True) #文章正文

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']

class Comment(models.Model):
    article = models.ForeignKey(Article)
    create_date = models.DateTimeField(auto_now_add=True) #发布评论时间
    content = models.TextField(blank=True) # Comments
    
