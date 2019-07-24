from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


# Create your models here.

class Tag(models.Model):
    """每一篇文章的标签"""
    tag_name = models.CharField(max_length=20, blank=True, help_text='标签的名称', verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = 'sblog_tag'
        verbose_name = '标签'


class Author(models.Model):
    """这是博客系统拓展的系统用户"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='作者关联的系统账号', verbose_name='账号')
    pen_name = models.CharField(max_length=30, help_text='作者的笔名（显示的作者名）', verbose_name='笔名')
    website = models.URLField(blank=True, help_text='作者的个人主页链接', verbose_name='主页')

    def __str__(self):
        return self.pen_name

    class Meta:
        db_table = 'sblog_author'
        verbose_name = '作者'


class Category(models.Model):
    """这是文章的分类model"""
    category_name = models.CharField(max_length=20, help_text='分类的名称', verbose_name='分类名称')
    category_slug = models.CharField(max_length=20, unique=True, help_text='分类的缩写', verbose_name='分类缩写')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'sblog_category'
        verbose_name = '分类'


class Blog(models.Model):
    """博客主题model"""
    caption = models.CharField(max_length=50, help_text='文章的标题', verbose_name='标题')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text='文章的作者', verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='文章的分类', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, help_text='文章的标签', verbose_name='标签')
    stick = models.BooleanField(default=False, help_text='文章的是否置顶', verbose_name='置顶')
    abstract = models.TextField(help_text='文章的摘要', verbose_name='摘要')
    content = RichTextUploadingField(help_text='文章的内容', verbose_name='内容')
    cover_image = models.ImageField(upload_to='uploads/%Y/%m/%d', help_text='文章的封面图片', verbose_name='封面')
    publish_time = models.DateTimeField(auto_now_add=True, help_text='文章的发布时间', verbose_name='发布时间')
    update_time = models.DateTimeField(auto_now=True, help_text='文章的更新时间', verbose_name='更新时间')
    visits = models.BigIntegerField(default=0, help_text='文章的浏览量', verbose_name='浏览量')

    def __str__(self):
        return u'%s %s %s' % (self.caption, self.author, self.publish_time)

    def image_tag(self):
        return mark_safe(u'<img src="%s" width="300px" />' % self.cover_image.url)

    image_tag.short_description = _('封面预览')

    class Meta:
        db_table = 'sblog_blog'
        ordering = ['-stick', '-publish_time']
        verbose_name = '文章'


class Constanter(models.Model):
    """常量表"""
    the_key = models.CharField(max_length=50, help_text='常亮的键', verbose_name='键', unique=True, null=False)
    the_value = models.CharField(max_length=200, help_text='常亮的值', verbose_name='值')
    descriptions = models.TextField(help_text='常亮的描述', verbose_name='描述')

    def __str__(self):
        return '常量[%s]' % self.the_key

    class Meta:
        db_table = 'sblog_constanter'
        verbose_name = '常量'


class Album(models.Model):
    """相册表"""
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d', help_text='照片', verbose_name='照片')
    remark = models.TextField(help_text='照片备注', verbose_name='备注')
    publish_time = models.DateTimeField(auto_now_add=True, help_text='照片的发布时间', verbose_name='发布时间')
    public = models.BooleanField(default=True, help_text='照片是否公开', verbose_name='公开')

    def image_tag(self):
        return mark_safe(u'<img src="%s" width="300px" />' % self.photo.url)

    image_tag.short_description = _('照片预览')

    def __str__(self):
        return '照片[%s]' % self.remark

    class Meta:
        db_table = 'sblog_album'
        ordering = ['-publish_time']
        verbose_name = '相册'
