from django.contrib import admin
from django.db import models
from .models import Article, ArticleCategory, Comment, ArticleLevel, ArticleTag
from django.forms import Textarea

# Register your models here.

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'published',
        'created_at',
        'comments_count',
    )

    list_filter = (
        'category__name',
        'published',
    )

    autocomplete_fields = ['category']

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 90})},
    }

    def comments_count(self, obj):
        return Comment.objects.filter(article=obj).count()
    comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    search_fields = ['article__title', 'author_name', ]
    list_display = (
        'article',
        'author_name',
        'status',
        'moderation_text',
        'created_at',
        'text',
    )

    list_editable = ('status', 'moderation_text', )
    list_filter = ('status', )


@admin.register(ArticleLevel)
class LevelAdmin(admin.ModelAdmin):
    search_fields = ['article__title', 'author_name']


@admin.register(ArticleTag)
class TagAdmin(admin.ModelAdmin): pass