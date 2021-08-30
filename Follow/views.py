from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FollowQuestionSerializer
from .models import FollowQuestion

# Create your views here.


class NewQuestionFollow(generics.CreateAPIView):

  serializer_class = FollowQuestionSerializer
  queryset = FollowQuestion.objects.all()



class MyQuestionFollow(generics.ListAPIView):

  serializer_class = FollowQuestionSerializer

  def get_queryset(self):

    user_id = self.kwargs['user_id']
    question_id = self.kwargs['question_id']

    return FollowQuestion.objects.filter(user_id=user_id, question_id=question_id)

  
class DeleteMyQuestionFollow(APIView):

  def post(self, request, user_id, question_id):

    following_question = FollowQuestion.objects.get(user_id=user_id, question_id=question_id)

    following_question.delete()

    return Response({"message": "Successfully Deleted"})


