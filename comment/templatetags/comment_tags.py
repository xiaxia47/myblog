from ..models import Comment
from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    value.as_widget(attrs={'class':arg})
    #for item in value:
    #    item.field.widget.attrs.update({'class': arg})
    return value

