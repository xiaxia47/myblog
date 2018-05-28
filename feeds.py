from django.contrib.syndication.views import Feed
from article.models import Article

class AllArticlesRssFeed(Feed):
    title = "极致简洁博客"
    link = '/'
    description = "极致简洁博客的文章"
    
    def items(self):
        return Article.objects.all()
    
    def item_title(self, item):
        return f'[{item.category}] {item.title}'

    def item_description(self, item):
        return item.excerpt
