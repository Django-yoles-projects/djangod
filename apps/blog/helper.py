from .models import Article, ArticleCategory

article_category_all = ArticleCategory(name='All')


def get_category_and_articles(category_name):
    articles = Article.objects.filter(published=True)
    if category_name == article_category_all.slug():
        category = ArticleCategory(name=category_name)
    else:
        try:
            category = ArticleCategory.objects.get(name__iexact=category_name)
            articles = articles.filter(category=category)
        except ArticleCategory.DoesNotExist:
            category = ArticleCategory(name=category_name)
            articles = Article.objects.none()

    articles = articles.order_by('-created_at')
    return category, articles


def get_categories():
    categories = list(ArticleCategory.objects.all().order_by('name'))
    categories.insert(0, article_category_all)
    return categories