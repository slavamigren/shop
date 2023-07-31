from django.contrib import admin

from blog.models import Blog

@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'text', 'avatar', 'created', 'is_published', 'views_count')
    list_filter = ('title',)

