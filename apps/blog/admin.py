from django.contrib import admin
from .models import Post, PostCategory

# Register your models here.

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'published',
        'created_at',
    )

    list_filter = (
        'category__name',
        'published',
    )

    autocomplete_fields = ['category']