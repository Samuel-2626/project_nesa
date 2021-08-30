from django.urls import path
from .views import ask_question, question_list, question_detail, edit_question, delete_question, edit_answer, delete_answer, QuestionCounter, QuestionVoteList, QuestionCreateVote, ChangeQuestionCounter, QuestionVoteUpDetail, QuestionVoteDownDetail, ChangeAnswerAcceptedSerializer, AnswerCounter, AnswerVoteList, AnswerCreateVote, ChangeAnswerCounter, AnswerVoteUpDetail, AnswerVoteDownDetail, NotificationCreate, ProfileUpdatePlus, ProfileUpdateMinus, question_list_top, question_list_top_views, question_search, question_share


app_name = 'questions'

urlpatterns = [

    # django rest framework urls
    path('question-change-status-upvote/<int:author_id>/<int:question_id>/', QuestionVoteUpDetail.as_view()),
    path('question-change-status-downvote/<int:author_id>/<int:question_id>/', QuestionVoteDownDetail.as_view()),
    path('question-counter/<int:pk>/', QuestionCounter.as_view(), name='question-counter'),
    path('question-vote-create/', QuestionCreateVote.as_view()),
    path('question-vote-detail/<int:user_id>/<int:question_id>/', QuestionVoteList.as_view(), name='question-vote-detail'),
    path('change-question-counter/<int:pk>/', ChangeQuestionCounter.as_view()),
    path('change-answer-accepted/<int:pk>/', ChangeAnswerAcceptedSerializer.as_view()),

    path('answer-counter/<int:pk>/', AnswerCounter.as_view()),

    path('answer-vote-list/<int:user_id>/<int:answer_id>/', AnswerVoteList.as_view()),
    path('answer-vote-create/', AnswerCreateVote.as_view()),    
    path('change-answer-counter/<int:pk>/', ChangeAnswerCounter.as_view()),

    path('answer-change-status-upvote/<int:author_id>/<int:answer_id>/', AnswerVoteUpDetail.as_view()),
    path('answer-change-status-downvote/<int:author_id>/<int:answer_id>/', AnswerVoteDownDetail.as_view()),

    path('notification/<int:user_id>/<str:message>/', NotificationCreate.as_view()),
    path('profile-plus/<int:user_id>/', ProfileUpdatePlus.as_view()),
    path('profile-minus/<int:user_id>/', ProfileUpdateMinus.as_view()),
    


    # django urls
    path('search/', question_search, name='question_search'),
    path('ask/', ask_question, name='ask-question'),
    path('', question_list, name='question-list'),
    path('top/', question_list_top, name='question-list-top'),
    path('most-views/', question_list_top_views, name='question-list-top-views'),
    path('tag/<slug:tag_slug>/', question_list, name='question_list_by_tag'),
    path('<slug:slug>/', question_detail, name='question-detail'),
    path('<slug:slug>/edit/', edit_question, name='edit_question'),
    path('<slug:slug>/delete/', delete_question, name='delete_question'),
    path('<int:id>/edit/<slug:slug>/', edit_answer, name='edit_answer'),
    path('<int:id>/delete/<slug:slug>/', delete_answer, name='delete_answer'),
    path('<slug:question_slug>/share/', question_share, name='question_share'),
    
    

    
]

