# coding:utf8

from django.conf.urls import url
from . import views

app_name = 'msblog'

urlpatterns = [
    url(r'^$', views.blog_home, name='home'),
    url(r'^category/(?P<category_slug>\w+)$', views.blog_category, name='category'),
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^shuo$', views.blog_shuo, name='shuo'),
    url(r'^album$', views.blog_album, name='album'),
    url(r'^board$', views.blog_board, name='board'),
    url(r'^article/(?P<blog_id>[0-9]+)$', views.blog_detail, name='detail'),
]
