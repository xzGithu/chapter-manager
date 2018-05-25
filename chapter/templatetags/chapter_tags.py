from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from chapter.models import Post

@register.simple_tag
def total_post():
    return Post.published.count()

@register.inclusion_tag('blog/latest_post.html')
def show_latest_post(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_post":latest_posts}

@register.assignment_tag
def most_commtents_post(count=5):
    return Post.published.annotate(total_comments=Count('postcomments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))