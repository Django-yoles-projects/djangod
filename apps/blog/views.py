from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from django.shortcuts import get_object_or_404, render
from .models import Article, Comment
from . import helper

# Create your views here.
def home_page(request, category_name=helper.article_category_all.slug()):
    categories = helper.get_categories()
    category, articles = helper.get_category_and_articles(category_name)

    context = {
        'category': category,
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'core/home.html', context)


def article_detail(request, article_id, message=''):
    article = get_object_or_404(Article, pk=article_id)
    articles_same_category = Article.objects.filter(published=True, category=article.category)\
        .exclude(pk=article_id)
    comments = article.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()

            args = [article.pk, 'Votre commentaire à bien été posté!']
            return HttpResponseRedirect(reverse('blog:article_detail_message', args=args) + '#comments')
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'articles_same_category': articles_same_category,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
    }
    return render(request, 'blog/article_detail.html', context)