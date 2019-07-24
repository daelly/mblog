from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from msblog.models import *


# Register your models here.

class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'author'


class UserAdmin(BaseUserAdmin):
    inlines = (AuthorInline,)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'pen_name', 'website')
    search_fields = ('pen_name',)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('caption', 'category', 'author', 'stick', 'publish_time')
    exclude = ('visits',)
    readonly_fields = ('image_tag',)
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)


class AlbumAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Constanter)
