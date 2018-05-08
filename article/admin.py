from django.contrib import admin
from .models import Article

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date')
    fieldsets = [
        (None,{'fields':['title']}),
        ('类别',{'fields':['category']}),
        ('详细信息',{'fields':['content'],'classes':['collapse']})
    ]
    list_filter= ['category']
    search_fields=['title','category']

