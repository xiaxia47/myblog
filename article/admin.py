from django.contrib import admin
from .models import Article, Tag, Category

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date')
    fieldsets = [
        (None,{'fields':['title']}),
        ('类别',{'fields':['category','tag']}),
        ('详细信息',{'fields':['author','excerpt','content'],'classes':['collapse']})
    ]
    list_filter= ['category','tag']
    search_fields=['title','category','tag']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

