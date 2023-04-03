# System libraries
import socket

# Third-party libraries
from taggit.models import Tag
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Django modules
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Django apps
from account.models import Profile
from notification.models import Notification
from Follow.models import FollowQuestion
from notification.models import Notification, Observer

# Current-app modules
from .models import Question, Answer, QuestionVotes, VoteAnswer, QuestionViews
from .forms import QuestionForm, AnswerForm, EmailPostForm
from .serializers import QuestionSerializer, QuestionVoteSerializer, AnswerSerializer, VoteAnswerSerializer


@login_required
def ask_question(request):
    """   A django function to enable logged in users to ask question  """

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    # set new question to none
    new_question = None

    # check if request method is equal post
    if request.method == 'POST':

        # create an instance of the form passing in the data the user submitted
        question_form = QuestionForm(data=request.POST)

        # check of the form is valid
        if question_form.is_valid():

            # set new question to the details the user submitted, but do not save in database yet
            new_question = question_form.save(commit=False)

            # set the author of the question to the user submitting the form
            new_question.author = request.user

            if request.user.profile.reputation >= 50:
                new_question.status = 'published'

                new_question.save()

                question_form.save_m2m()

                # get the profile of the current user
                user_profile = Profile.objects.get(user=request.user)

                # give the user 5 reputation for asking a question
                user_profile.reputation += 5

                # save this new reputation
                user_profile.save()

                new_notificatiion = Notification.objects.create(
                    user=request.user, message=f'Hi {request.user.first_name}, your question as been published, <a href="{ new_question.get_absolute_url() }">Check it out</a>. And you have received a whooping five points for your reputation, please share your question so others can answer')

                # save notification in database
                new_notificatiion.save()

                # send an email to the user
                send_mail('New Question [Nesa Academy Admin]', f'Hi {request.user.first_name}, \n\nYour question as been published and you have received a whooping five points for your reputation.\n\n {request.build_absolute_uri(new_question.get_absolute_url())} \n\nPlease share your question so others can answer. \n\nCheers.', f'{settings.DEFAULT_FROM_EMAIL}', [
                          request.user.email])

                messages.success(
                    request, 'Your question as been published, please share your question with others. <a href="/help/#ask-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')

                return redirect('questions:question-list')

            # save question now to the database
            new_question.save()

            # save the many-to-many data for the form.
            question_form.save_m2m()

            # create notification to send to that user
            new_notificatiion = Notification.objects.create(
                user=request.user, message=f'Hi {request.user.first_name}, we received your question. Great work!! we would review your question and if approved, it would be published immediately to the world')

            # save notification in database
            new_notificatiion.save()

            # send an email to the user
            send_mail('New Question [Nesa Academy Admin]', f'Hi {request.user.first_name}, \n\nWe have received your question and would be reviewed. \n\nIf it is approved, it would be published', f'{settings.DEFAULT_FROM_EMAIL}', [
                      request.user.email])

            # get the profile of the current user
            user_profile = Profile.objects.get(user=request.user)

            # give the user 2 reputation for asking a question
            user_profile.reputation += 2

            # save this new reputation
            user_profile.save()

            # create notification to tell the user of this new reputation
            new_notificatiion = Notification.objects.create(
                user=request.user, message=f'Hi {request.user.first_name}, you just earned an additional 2 points for your reputation. Great work!! Keep it going')

            # save the notification
            new_notificatiion.save()

            # send email to tell user of that new reputation
            send_mail('Additional Reputation [Nesa Academy Admin]',
                      f'Hi {request.user.first_name}, \n\nYou just earned an additional two points for your reputation.\n\nCheers.', f'{settings.DEFAULT_FROM_EMAIL}', [request.user.email])

            messages.success(
                request, 'Your question as been submitted for review. <a href="/help/#ask-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')

            return redirect('questions:question-list')

    else:
        question_form = QuestionForm()

    return render(request, 'questions/ask.html', {
        'question_form': question_form,
        'new_question': new_question,
        'total_notifications': total_notifications,
    })


def question_search(request):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    query = None
    results = []
    if 'query_question' in request.GET:

        query = request.GET.get('query_question')

        # search_vector = SearchVector('title', 'body')
        # search_query = SearchQuery(query)
        # results = Question.published.annotate(search=search_vector, rank=SearchRank(
        #     search_vector, search_query)).filter(search=search_query).order_by('-rank')

        results = Question.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    return render(request, 'questions/search.html', {

        'query': query,
        'results': results,

        'total_notifications': total_notifications,

    })


def question_list(request, tag_slug=None):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    try:
        user = User.objects.get(pk=request.user.pk)
    except:
        user = None

    object_list = Question.published.all()
    total = Question.published.all().count
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 100)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)

    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/list-question.html', {
        'questions': questions,
        'user': user,
        'page': page,
        'tag': tag,
        'total': total,
        'total_notifications': total_notifications,
    })


def question_list_top(request, tag_slug=None):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    try:
        user = User.objects.get(pk=request.user.pk)
    except:
        user = None

    object_list = Question.published.all().order_by('-counter')
    total = Question.published.all().count
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag]).order_by('-counter')
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/list-top-question.html', {
        'questions': questions,
        'page': page,
        'tag': tag,
        'total': total,
        'total_notifications': total_notifications,
        'user': user,
    })


def question_list_top_views(request, tag_slug=None):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    try:
        user = User.objects.get(pk=request.user.pk)
    except:
        user = None

    object_list = Question.published.all().order_by('-views')
    total = Question.published.all().count
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag]).order_by('-views')
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/list-top-views-question.html', {
        'questions': questions,
        'page': page,
        'tag': tag,
        'total': total,
        'total_notifications': total_notifications,
        'user': user,
    })


def question_detail(request, slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    question = get_object_or_404(Question, slug=slug,  status='published')

    hostname = socket.gethostname()

    ip_address = socket.gethostbyname(hostname)

    try:
        new_view = QuestionViews(
            question=question, host=hostname, ip=ip_address)
        new_view.save()
        question.views += 1
        question.save()

    except:
        pass

    try:
        user = User.objects.get(pk=request.user.pk)
    except:
        user = None

    # List of active answers for this post
    answers = question.answers.filter(status='published')

    new_answer = None

    try:
        if request.method == 'POST':

            answer_form = AnswerForm(data=request.POST)

            if answer_form.is_valid():

                new_answer = answer_form.save(commit=False)
                new_answer.question = question
                new_answer.author = request.user

                if request.user.profile.reputation >= 50:
                    new_answer.status = 'published'
                    new_answer.save()
                    answer_form.save_m2m()

                    try:

                        followers = FollowQuestion.objects.filter(
                            question=question)

                        for follower in followers:

                            new_notificatiion = Notification.objects.create(
                                user=follower.user, message=f'Hi {follower.user.first_name}, a new answer was posted for question titled "{question.title}", <a href="{ question.get_absolute_url() }">Check it out</a>. Note that you are receiving this notification because you follow this question.')

                            new_notificatiion.save()

                    except:
                        pass

                    user_profile = Profile.objects.get(user=request.user)

                    user_profile.reputation += 5

                    user_profile.save()

                    new_notificatiion = Notification.objects.create(
                        user=request.user, message=f'Hi {request.user.first_name}, your answer as been published for question titled "{question.title}" and you received a whooping five points for your reputation')

                    new_notificatiion.save()

                    send_mail('Answered Published [Nesa Academy Admin]', f'Hi, {request.user.first_name}, \n\nYour answer as been published and you received a whooping five points for your reputation. \n\nCheers.', f'{settings.DEFAULT_FROM_EMAIL}', [
                              request.user.email])

                    messages.success(request, 'Your answer as been published')
                    return redirect('questions:question-detail', slug=slug)

                new_answer.save()
                answer_form.save_m2m()

                new_notificatiion = Notification.objects.create(
                    user=request.user, message=f'Hi {request.user.first_name}, your answer as been submitted for review. If approved it would be published')

                new_notificatiion.save()

                send_mail('Answered Drafted [Nesa Academy Admin]', f'Hi, {request.user.first_name}, \n\nYour answer as been submitted for review.\n\nIf approved it would be published to the world.', f'{settings.DEFAULT_FROM_EMAIL}', [
                          request.user.email])

                user_profile = Profile.objects.get(user=request.user)

                user_profile.reputation += 2

                user_profile.save()

                new_notificatiion = Notification.objects.create(
                    user=request.user, message=f'Hi {request.user.first_name}, you just earned additional 2 points for your reputation. Great work!! Keep it going')

                new_notificatiion.save()

                send_mail('Great news [Nesa Academy Admin]', f'Hi, {request.user.first_name}, \n\nYou just earned additional two points for your reputation. \n\nGreat work!! Keep it going', f'{settings.DEFAULT_FROM_EMAIL}', [
                          request.user.email])

            else:

                messages.success(request, 'The form can\'t be empty')
                return redirect('questions:question-detail', slug=slug)

    except:
        messages.success(request, '<strong>Access Denied:</strong> You have already answered this question  <a href="/help/#how-to-answer-a-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    else:
        answer_form = AnswerForm()

    question_tags_ids = question.tags.values_list('id', flat=True)
    similar_questions = Question.published.all().filter(
        tags__in=question_tags_ids).exclude(id=question.id)
    similar_questions = similar_questions.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-created')[:20]

    return render(request, 'questions/detail-question.html', {
        'question': question,
        'new_answer': new_answer,
        'answer_form': answer_form,
        'answers': answers,
        'similar_questions': similar_questions,
        'user': user,
        'total_notifications': total_notifications,
    })


@login_required
def edit_question(request, slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    item = Question.objects.get(slug=slug, status='published')

    if item.author != request.user:
        messages.success(
            request, '<strong>Access Denied:</strong> You are not the author of this question ', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.user.profile.reputation < 49:
        messages.success(request, '<strong>Access Denied:</strong> Only people with over 50 reputation can edit a question <a href="/help/#editing-a-question-or-answer" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST, instance=item)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            question_form.save_m2m()

            try:

                followers = FollowQuestion.objects.filter(question=item)

                for follower in followers:

                    new_notificatiion = Notification.objects.create(
                        user=follower.user, message=f'Hi {follower.user.first_name}, the question titled "{item.title}" was edited, <a href="{item.get_absolute_url() }">Check it out</a> . Note that you are receiving this notification because you follow this question.')

                    new_notificatiion.save()

            except:
                pass

            messages.success(request, 'question edited successfully!')
            return redirect('questions:question-detail', slug=slug)

    else:
        question_form = QuestionForm(instance=item)

    return render(request, 'questions/edit.html', {
        'question_form': question_form,
        'total_notifications': total_notifications,
        'item': item,
    })


@login_required
def delete_question(request, slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    item = Question.objects.get(slug=slug, status='published')

    total_answers = item.answers.count()

    if item.author != request.user:
        messages.success(
            request, '<strong>Access Denied:</strong> You are not the author of this question', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if total_answers >= 1:
        messages.success(request, '<strong>Access Denied:</strong> You can\'t delete a question that has an approved answer :) <a href="/help/#deleting-a-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.user.profile.reputation < 99:
        messages.success(request, '<strong>Access Denied:</strong> Only people with over 100 reputation can delete a question <a href="/help/#deleting-a-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.method == 'POST':
        item.delete()
        try:

            followers = FollowQuestion.objects.filter(question=item)

            for follower in followers:

                new_notificatiion = Notification.objects.create(
                    user=follower.user, message=f'Hi {follower.user.first_name}, the question titled "{item.title}" as been deleted by the author, automatically you don\'t follow this question again. Note that you are receiving this notification because you follow this question.')

                new_notificatiion.save()

        except:
            pass
        messages.success(request, 'question deleted successfully!')
        return redirect('questions:question-list')

    else:
        question_form = QuestionForm()

    return render(request, 'questions/delete.html', {
        'question_form': question_form,
        'item': item,

        'total_notifications': total_notifications,
    })


@login_required
def edit_answer(request, id, slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    answer = Answer.objects.get(pk=id, status='published')
    question = Question.objects.get(slug=slug, status='published')
    slug = question.slug

    if request.user.profile.reputation < 49:
        messages.success(request, '<strong>Access Denied:</strong> Only people with over 50 reputation can edit an answer <a href="/help/#editing-a-question-or-answer" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if answer.author != request.user:
        messages.success(
            request, 'Access Denied: You are not the author of this answer')
        return redirect('questions:question-detail', slug=slug)

    if request.method == 'POST':
        answer_form = AnswerForm(data=request.POST, instance=answer)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.author = request.user

            new_answer.save()

            try:

                followers = FollowQuestion.objects.filter(question=question)

                for follower in followers:

                    new_notificatiion = Notification.objects.create(
                        user=follower.user, message=f'Hi {follower.user.first_name}, an answer was edited for question titled "{question.title}", <a href="{question.get_absolute_url() }">Check it out</a> . Note that you are receiving this notification because you follow this question.')

                new_notificatiion.save()

            except:
                pass

            messages.success(request, 'answer edited successfully!')
            return redirect('questions:question-detail', slug=slug)

    else:
        answer_form = AnswerForm(instance=answer)

    return render(request, 'questions/edit_answer.html', {
        'answer_form': answer_form,
        'answer': answer,
        'total_notifications': total_notifications,
        'question': question,
    })


@login_required
def delete_answer(request, id, slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    answer = Answer.objects.get(pk=id)
    question = Question.objects.get(slug=slug)

    if answer.author != request.user:
        messages.success(
            request, '<strong>Access Denied:</strong> You are not the author of this answer', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if answer.accepted == True:
        messages.success(
            request, '<strong>Access Denied:</strong> You cannot delete an answer already accepted by the author of the question', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.user.profile.reputation < 99:
        messages.success(request, '<strong>Access Denied:</strong> Only people with over 500 reputation can delete a question <a href="/help/#deleting-a-question" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')
        return redirect('questions:question-detail', slug=slug)

    if request.method == 'POST':
        answer.delete()
        try:

            followers = FollowQuestion.objects.filter(question=question)

            for follower in followers:

                new_notificatiion = Notification.objects.create(
                    user=follower.user, message=f'Hi {follower.user.first_name}, an answer was deleted for question titled "{question.title}", <a href="{ question.get_absolute_url() }">Check it out</a> . Note that you are receiving this notification because you follow this question.')

                new_notificatiion.save()

        except:
            pass
        messages.success(request, 'answer deleted successfully!')
        return redirect('questions:question-detail', slug=slug)

    else:
        answer_form = AnswerForm()

    return render(request, 'questions/delete_answer.html', {
        'answer_form': answer_form,
        'answer': answer,
        'total_notifications': total_notifications,
        'question': question,
    })


def question_share(request, question_slug):

    if request.user.id != None:

        try:
            observer = Observer.objects.get(user=request.user)
            total_notifications = Notification.objects.filter(
                user=request.user, date__gt=observer.date).count

        except:
            total_notifications = Notification.objects.filter(
                user=request.user).count
    else:
        total_notifications = None

    # Retrieve post by id
    question = get_object_or_404(
        Question, slug=question_slug, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            question_url = request.build_absolute_uri(
                question.get_absolute_url())
            subject = f"{cd['name']} recommends you to view this question on Nesa Academy '{question.title}'"
            message = f"Read {question.title} at {question_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message,
                      f'{settings.DEFAULT_FROM_EMAIL}', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'questions/share.html', {
        'question': question,
        'form': form,
        'sent': sent,
        'total_notifications': total_notifications,
    })


"""  Django Rest API Views """


class QuestionCounter(generics.RetrieveAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCreateVote(generics.ListCreateAPIView):

    queryset = QuestionVotes.objects.all()
    serializer_class = QuestionVoteSerializer


class QuestionVoteList(generics.ListAPIView):

    serializer_class = QuestionVoteSerializer

    def get_queryset(self):

        user_id = self.kwargs['user_id']
        question_id = self.kwargs['question_id']

        return QuestionVotes.objects.filter(author__pk=user_id, question_id=question_id)


class QuestionVoteUpDetail(APIView):

    def post(self, request, author_id, question_id):

        question_vote = QuestionVotes.objects.get(
            author__pk=author_id, question_id=question_id)

        question_vote.status = 'upvote'

        question_vote.save()

        return Response({"message": "Status Updated from downvote to an upvote"})


class QuestionVoteDownDetail(APIView):

    def post(self, request, author_id, question_id):

        question_vote = QuestionVotes.objects.get(
            author__pk=author_id, question_id=question_id)

        question_vote.status = 'downvote'

        question_vote.save()

        return Response({"message": "Status Updated from upvote to a downvote"})


class ChangeQuestionCounter(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChangeAnswerAcceptedSerializer(generics.UpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerCounter(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerVoteList(generics.ListAPIView):

    serializer_class = VoteAnswerSerializer

    def get_queryset(self):

        user_id = self.kwargs['user_id']
        answer_id = self.kwargs['answer_id']

        return VoteAnswer.objects.filter(author__pk=user_id, answer_id=answer_id)


class AnswerCreateVote(generics.ListCreateAPIView):

    queryset = VoteAnswer.objects.all()
    serializer_class = VoteAnswerSerializer


class ChangeAnswerCounter(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerVoteUpDetail(APIView):

    def post(self, request, author_id, answer_id):

        answer_vote = VoteAnswer.objects.get(
            author__pk=author_id, answer_id=answer_id)

        answer_vote.status = 'upvote'

        answer_vote.save()

        return Response({"message": "Status Updated from downvote to an upvote"})


class AnswerVoteDownDetail(APIView):

    def post(self, request, author_id, answer_id):

        answer_vote = VoteAnswer.objects.get(
            author__pk=author_id, answer_id=answer_id)

        answer_vote.status = 'downvote'

        answer_vote.save()

        return Response({"message": "Status Updated from upvote to a downvote"})


class NotificationCreate(APIView):

    def post(self, request, user_id, message):

        user = User.objects.get(pk=user_id)

        new_notification = Notification(user=user, message=message)

        new_notification.save()

        return Response({"success": "true"})


class ProfileUpdatePlus(APIView):

    def post(self, request, user_id):

        user = User.objects.get(pk=user_id)

        profile = Profile.objects.get(user=user)

        profile.reputation += 3

        profile.save()

        return Response({"success": "true"})


class ProfileUpdateMinus(APIView):

    def post(self, request, user_id):

        user = User.objects.get(pk=user_id)

        profile = Profile.objects.get(user=user)

        profile.reputation -= 3

        profile.save()

        return Response({"success": "true"})
