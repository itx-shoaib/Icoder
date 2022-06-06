from django import template

register = template.Library()

@register.filter(name='get_val') #used in blogPost for display the replies
def get_val(dict,key):
    return dict.get(key)