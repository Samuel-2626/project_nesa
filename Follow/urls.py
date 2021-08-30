from django.urls import path
from . import views

urlpatterns = [
    path('new_question_follow/', views.NewQuestionFollow.as_view()),
    path('my_question_follow/<int:user_id>/<int:question_id>/', views.MyQuestionFollow.as_view()),
    path('delete_question_follow/<int:user_id>/<int:question_id>/', views.DeleteMyQuestionFollow.as_view())
]
