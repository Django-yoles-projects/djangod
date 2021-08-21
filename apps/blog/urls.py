from django.urls import path, include
from django.shortcuts import render
from apps.blog.views import  home_page, article_detail

app_name = "blog"

urlpatterns = [
    # path('', get_article_list, name="home")
    path('', home_page, name="home"),
    path('category/<str:category_name>/', home_page, name='home_cat_selected'),
    path('articles/detail/<int:article_id>/', article_detail, name='article_detail'),
    path('articles/detail/<int:article_id>/<str:message>/', article_detail, name='article_detail_message'),
]