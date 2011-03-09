from django.contrib import admin

from caktus_website.blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('date', 'published')

admin.site.register(Post, PostAdmin)
