from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [

    # django REST framework views
    path('get_user_status/<int:user_id>/<int:post_id>/', views.GetPostUserStatus.as_view()),
    path('like_post/<int:user_id>/<int:post_id>/', views.LikePost.as_view()),
    path('dislike_post/<int:user_id>/<int:post_id>/', views.DisLikePost.as_view()),
    path('increase_article/<int:post_id>/', views.IncreaseArticle.as_view()),
    path('increase_dislike_article/<int:post_id>/', views.IncreaseDislikeArticle.as_view()),
    path('decrease_article/<int:post_id>/', views.DecreaseArticle.as_view()),
    path('decrease_dislike_article/<int:post_id>/', views.DecreaseDislikeArticle.as_view()),
    path('change-dislike-to-like/<int:user_id>/<int:post_id>/', views.RemoveDislikeToLike.as_view()),
    path('change-like-to-dislike/<int:user_id>/<int:post_id>/', views.RemoveLikeToDisLike.as_view()),



    # post views

    path('', views.post_list, name='post_list'),
    path('search/', views.article_search, name='article_search'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('new/', views.post_article, name='post_article'),
    path('comment/<int:id>/<slug:slug>/edit', views.edit_comment, name="edit_comment"),
    path('comment/<int:id>/<slug:slug>/delete', views.delete_comment, name="delete_comment"),

]
