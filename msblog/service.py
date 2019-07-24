# coding:utf8

from msblog.models import Blog, Constanter
from django.core.cache import cache
from django.shortcuts import get_object_or_404

_constant_key_ = '_constant_key_'


def hot_blogs(size):
    blogs = Blog.objects.all()[:size]
    return blogs


def visit_blogs(size):
    blogs = Blog.objects.order_by('-visits').all()[:size]
    return blogs


def lastest_blogs(size):
    blogs = Blog.objects.order_by('-update_time').all()[:size]
    return blogs


def constanter():
    constants = cache.get(_constant_key_)
    if constants:
        return constants
    constants = Constanter.objects.all()
    dicct = {}
    for item in constants:
        k = item.the_key
        v = item.the_value
        dicct[k] = v
    cache.set(_constant_key_, dicct)
    return dicct


def get_const(key):
    constants = constanter()
    return constants.get(key)


def reset_cache():
    constants = Constanter.objects.all()
    dicct = {}
    for item in constants:
        k = item.the_key
        v = item.the_value
        dicct[k] = v
    cache.set(_constant_key_, dicct)


def add_visit_count(blog_id, ip=None):
    key = 'blog_visits_of_' + blog_id
    cache.set(key, 0)
    visits = cache.incr(key)
    return visits


def get_blog_and_add_visits(blog_id):
    key = 'specified_blog_of_' + blog_id
    blog = cache.get(key)
    if not blog:
        blog = get_object_or_404(Blog, pk=blog_id)
        tags = blog.tags.all()
        tagnames = []
        for tag in tags:
            tagnames.append(tag.tag_name)

        blog.tagnames = tagnames
        prev_blog = Blog.objects.filter(id__lt=blog.id).values('id', 'caption').order_by('-id')[0:1]
        next_blog = Blog.objects.filter(id__gt=blog.id).values('id', 'caption').order_by('id')[0:1]
        blog.prev = prev_blog.get() if len(prev_blog) > 0 else None
        blog.next = next_blog.get() if len(next_blog) > 0 else None
        related = Blog.objects.filter(tags__blog__tags__in=tags).exclude(id=blog.id).values('id', 'caption').distinct().order_by('-update_time')[0:10]
        blog.related = related
        cache.set(key, blog)
    blog.visits = add_visit_count(blog_id)
    return blog
