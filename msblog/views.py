# coding:utf8

from django.shortcuts import render

from msblog.models import Blog, Category, Album
from msblog import service
from django.template.defaultfilters import register
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from mblog.settings import SYSTEM_SKIN_NAME
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

skin = SYSTEM_SKIN_NAME
page_size = 9


@register.filter(name='cstrip')
def content_breviary(content, size):
    if not content:
        content = ''
    # 替换注释
    content = re.sub(r'<!--(?!-->).*-->', '', content)
    # 替换标签
    content = re.sub(r'<.*?>', '', content)
    if content and len(content) > size:
        return content[:size] + "..."
    else:
        return content


# 主页
def blog_home(request):
    blogs = service.hot_blogs(5)
    lastest = service.lastest_blogs(8)
    suggestion = service.visit_blogs(8)
    return render(request, skin + '/home.html', {'blogs': blogs, 'lastest': lastest, 'suggestion': suggestion})


class AboutView(TemplateView):
    template_name = skin + '/about.html'


def blog_shuo(request):
    return render(request, skin + '/shuo.html', {})


def blog_album(request):
    lastest = service.lastest_blogs(8)
    suggestion = service.visit_blogs(8)
    photos = Album.objects.all()
    return render(request, skin + '/album.html', {'lastest': lastest, 'suggestion': suggestion, 'photos': photos})


def blog_board(request):
    return render(request, 'board.html', {})


@cache_page(30 * 60, key_prefix=skin)
def blog_category(request, category_slug):
    category = Category.objects.get(category_slug=category_slug)
    blog_list = Blog.objects.filter(category__category_slug=category_slug)
    paginator = Paginator(blog_list, page_size)
    lastest = service.lastest_blogs(8)
    suggestion = service.visit_blogs(8)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    return render(request, skin + '/list.html',
                  {'page': page, 'blogs': blogs, 'category': category, 'lastest': lastest, 'suggestion': suggestion})


@cache_page(60 * 60 * 24, key_prefix=skin)
def blog_detail(request, blog_id):
    article = service.get_blog_and_add_visits(blog_id)
    visits = service.visit_blogs(8)
    suggestion = service.hot_blogs(8)
    return render(request, skin + '/blog.html', {'article': article, 'visits': visits, 'suggestion': suggestion})
