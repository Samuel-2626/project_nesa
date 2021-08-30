from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/questions', views.questions, name='questions'),
    path('dashboard/answers', views.answers, name='answers'),
    path('dashboard/articles', views.articles, name='articles'),
    path('dashboard/followed/question',
         views.followed_questions, name='followed-questions'),
    path('dashboard/liked/articles',
         views.liked_articles, name='liked-articles'),
    path('dashboard/articles/<int:id>/delete',
         views.delete_article, name='delete_article'),
    path('dashboard/articles/<int:id>/edit',
         views.edit_article, name='edit_article'),
    path('profile/<int:id>/<str:username>',
         views.show_profile, name='profile'),
    path('edit/', views.update_profile, name='edit'),
    path('delete/', views.delete_profile, name='delete'),
    path('dashboard/question/<int:id>',
         views.question_detail, name='admin-question-detail'),
    path('dashboard/answer/<int:id>',
         views.answer_detail, name='admin-answer-detail'),
    path('dashboard/question/<int:id>/approve',
         views.approve_question, name='approve-question'),
    path('dashboard/answer/<int:id>/approve',
         views.approve_answer, name='approve-answer'),
    path('admin/message/<int:id>', views.message, name='message-admin'),
    path('admin/message-for-answer/<int:id>',
         views.message_for_answer, name='message-for-answer'),
    path('admin/delete/<int:id>', views.delete, name='delete-question-admin'),
    path('admin/delete-answer/<int:id>',
         views.delete_answer, name='delete-answer-admin'),

    path('dashboard/questions/published',
         views.published_questions, name='published-questions'),
    path('dashboard/questions/draft',
         views.draft_questions, name='draft-questions'),
    path('dashboard/questions/draft/<int:id>/delete',
         views.delete_draft_questions, name='delete-draft-questions'),

    path('dashboard/questions/draft/<int:id>/edit',
         views.edit_draft_questions, name='edit-draft-questions'),

    path('dashboard/answers/published',
         views.published_answers, name='published-answers'),
    path('dashboard/answers/draft', views.draft_answers, name='draft-answers'),

    path('dashboard/answers/draft/<int:id>/delete',
         views.delete_draft_answers, name='delete-draft-answers'),

    path('dashboard/answers/draft/<int:id>/edit',
         views.edit_draft_answers, name='edit-draft-answers'),

    path('dashboard/empty/notification/',
         views.empty_notification, name='empty-notification'),

]
