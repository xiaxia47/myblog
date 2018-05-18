from ..models import Article, Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Article.objects.all().order_by('-pub_date')[:num]

@register.simple_tag
def archives():
    return Article.objects.dates('pub_date', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()
