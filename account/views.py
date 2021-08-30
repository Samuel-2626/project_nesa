# System Libraries
import socket
from datetime import timedelta

# Third-party Libraries

# Django modules
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Django apps
from questions.models import Question, Answer
from account.models import Profile
from notification.models import Notification
from articles.models import Article, PostLikesOrDislikes
from articles.forms import PostForm
from questions.forms import QuestionForm, AnswerForm
from Follow.models import FollowQuestion
from notification.models import Notification, Observer

# Current-app modules
from .forms import ProfileForm, MessageForm
from .models import Profile, ProfileViews


@login_required
def dashboard(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    user = User.objects.get(id=request.user.id)
    questions = Question.objects.filter(status='draft')
    answers = Answer.objects.filter(status='draft')

    followed_question = FollowQuestion.objects.filter(user=request.user)

    liked_articles = PostLikesOrDislikes.objects.filter(
        author=request.user, status='like')

    return render(request,
                  'account/dashboard.html', {
                      'user': user,
                      'questions': questions,
                      'answers': answers,
                      'auth0User': auth0user,
                      'total_notifications': total_notifications,
                      'followed_question': followed_question,
                      'liked_articles': liked_articles,
                  })


def liked_articles(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    liked_articles = PostLikesOrDislikes.objects.filter(
        author=request.user, status='like')

    return render(request,
                  'account/liked-articles.html', {

                      'auth0User': auth0user,

                      'liked_articles': liked_articles,

                      'total_notifications': total_notifications,
                  })


def followed_questions(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    followed_questions = FollowQuestion.objects.filter(user=request.user)

    return render(request,
                  'account/followed-question.html', {

                      'auth0User': auth0user,

                      'followed_questions': followed_questions,

                      'total_notifications': total_notifications,
                  })


@login_required
def articles(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    published_article = Article.objects.filter(
        status='published', author=request.user)

    return render(request,
                  'account/articles.html', {

                      'auth0User': auth0user,

                      'published_article': published_article,

                      'total_notifications': total_notifications,
                  })


@login_required
def delete_article(request, id):

    article = get_object_or_404(Article, pk=id)

    if article.author != request.user:
        messages.success(request, 'You are not the author of this article')
        return redirect('articles')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':

        article.delete()

        messages.success(request, 'successfully deleted')
        return redirect('articles')

    else:
        pass

    return render(request, 'account/delete-article.html', {
        'auth0User': auth0user,
        'article': article,
        'total_notifications': total_notifications,
    })


@login_required
def edit_article(request, id):

    article = get_object_or_404(Article, pk=id)

    if article.author != request.user:
        messages.success(request, 'You are not the author of this article')
        return redirect('articles')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':

        article_form = PostForm(
            data=request.POST, files=request.FILES, instance=article)

        if article_form.is_valid():
            new_article = article_form.save(commit=False)
            new_article.author = request.user
            new_article.status = 'published'
            new_article.save()
            article_form.save_m2m()

            messages.success(request, 'successfully edited')
            return redirect('articles')

    else:
        article_form = QuestionForm(instance=article)

    return render(request, 'account/edit-article.html', {
        'auth0User': auth0user,
        'article_form': article_form,
        'article': article,
        'total_notifications': total_notifications,
    })


@login_required
def questions(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    published_question = Question.objects.filter(
        status='published', author=request.user).count

    drafted_questions = Question.objects.filter(
        status='draft', author=request.user).count

    return render(request,
                  'account/questions.html', {

                      'auth0User': auth0user,

                      'published_question': published_question,
                      'drafted_questions': drafted_questions,
                      'total_notifications': total_notifications,
                  })


@login_required
def published_questions(request):

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

    total_questions = Question.published.all().count

    total_users = User.objects.filter(is_active=True).count
    total_articles = Article.published.all().count

    try:
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    questions = Question.objects.filter(
        author=request.user).filter(status='published')

    return render(request, 'account/published-question.html', {

        'total_questions': total_questions,

        'total_articles': total_articles,
        'total_users': total_users,

        'questions': questions,
        'total_notifications': total_notifications,

        'auth0User': auth0user,

    })


@login_required
def draft_questions(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    questions = Question.objects.filter(
        author=request.user).filter(status='draft')

    return render(request, 'account/draft-question.html', {

        'auth0User': auth0user,

        'questions': questions,
        'total_notifications': total_notifications,

    })


@login_required
def delete_draft_questions(request, id):

    question = get_object_or_404(Question, pk=id)

    if question.status == 'published':

        messages.success(request, 'This question is published already')
        return redirect('draft-questions')

    if question.author != request.user:
        messages.success(request, 'You are not the author of this question')
        return redirect('draft-questions')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    question = get_object_or_404(Question, pk=id)

    if request.method == 'POST':

        question.delete()

        messages.success(request, 'successfully deleted')
        return redirect('draft-questions')

    else:
        pass

    return render(request, 'account/delete-draft-question.html', {
        'auth0User': auth0user,
        'question': question,
        'total_notifications': total_notifications,
    })


@login_required
def edit_draft_questions(request, id):

    question = get_object_or_404(Question, pk=id)

    if question.status == 'published':

        messages.success(request, 'This question is published already')
        return redirect('draft-questions')

    if question.author != request.user:
        messages.success(request, 'You are not the author of this question')
        return redirect('draft-questions')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':

        question_form = QuestionForm(data=request.POST, instance=question)

        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.author = request.user
            new_question.status = 'draft'
            new_question.save()
            question_form.save_m2m()

            messages.success(request, 'successfully edited')
            return redirect('draft-questions')

    else:
        question_form = QuestionForm(instance=question)

    return render(request, 'account/edit-draft-question.html', {
        'auth0User': auth0user,
        'question_form': question_form,
        'total_notifications': total_notifications,
    })


@login_required
def answers(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    published_answers = Answer.objects.filter(
        status='published', author=request.user).count

    drafted_answers = Answer.objects.filter(
        status='draft', author=request.user).count

    return render(request,
                  'account/answers.html', {

                      'auth0User': auth0user,
                      'published_answers': published_answers,
                      'drafted_answers': drafted_answers,
                      'total_notifications': total_notifications,

                  })


@login_required
def published_answers(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answers = Answer.objects.filter(
        author=request.user).filter(status='published')

    return render(request, 'account/published-answers.html', {

        'auth0User': auth0user,

        'answers': answers,
        'total_notifications': total_notifications,

    })


@login_required
def draft_answers(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answers = Answer.objects.filter(author=request.user).filter(status='draft')

    return render(request, 'account/draft-answers.html', {

        'auth0User': auth0user,

        'answers': answers,
        'total_notifications': total_notifications,

    })


@login_required
def delete_draft_answers(request, id):

    answer = get_object_or_404(Answer, pk=id)

    if answer.status == 'published':

        messages.success(request, 'This answer is published already')
        return redirect('draft-answers')

    if answer.author != request.user:
        messages.success(request, 'You are not the author of this answer')
        return redirect('draft-answers')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':

        answer.delete()

        messages.success(request, 'successfully deleted')
        return redirect('draft-answers')

    else:
        pass

    return render(request, 'account/delete-draft-answer.html', {
        'auth0User': auth0user,
        'answer': answer,
        'total_notifications': total_notifications,
    })


@login_required
def edit_draft_answers(request, id):

    answer = get_object_or_404(Answer, pk=id)

    if answer.status == 'published':

        messages.success(request, 'This answer is published already')
        return redirect('draft-answers')

    if answer.author != request.user:
        messages.success(request, 'You are not the author of this answer')
        return redirect('draft-answers')

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':

        answer_form = AnswerForm(data=request.POST, instance=answer)

        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.author = request.user
            new_answer.status = 'draft'
            new_answer.save()
            answer_form.save_m2m()

            messages.success(request, 'successfully edited')
            return redirect('draft-answers')

    else:
        answer_form = AnswerForm(instance=answer)

    return render(request, 'account/edit-draft-answer.html', {
        'auth0User': auth0user,
        'answer_form': answer_form,
        'total_notifications': total_notifications,
    })


@login_required
def show_profile(request, id, username):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    hostname = socket.gethostname()

    ip_address = socket.gethostbyname(hostname)

    user = get_object_or_404(User, pk=id, username=username)
    profile = get_object_or_404(Profile, user=user)

    top_questions = Question.objects.filter(
        author=user, status='published').order_by('-counter')[:15]
    top_answers = Answer.objects.filter(
        author=user, status='published').order_by('-counter')[:15]
    top_articles = Article.objects.filter(
        author=user, status='published').order_by('-views')[:15]

    try:
        new_view = ProfileViews(profile=profile, host=hostname, ip=ip_address)
        new_view.save()
        profile.views += 1
        profile.save()
    except:
        pass

    questions = Question.published.all().filter(author__pk=id)
    answers = Answer.published.all().filter(author__pk=id)

    questions_count = questions.count()
    answers_count = answers.count()

    return render(request, 'account/profile.html', {
        'user': user,
        'questions': questions,
        'answers': answers,
        'questions_count': questions_count,
        'answers_count': answers_count,

        'top_questions': top_questions,
        'top_answers': top_answers,
        'top_articles': top_articles,

        'auth0User': auth0user,
        'total_notifications': total_notifications,

    })


@login_required
@transaction.atomic
def update_profile(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', id=request.user.id, username=request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {
        'profile_form': profile_form,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@transaction.atomic
def delete_profile(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    user = User.objects.get(username=request.user.username)

    if request.method == 'POST':

        user.delete()

        messages.success(request, 'successfully deleted')
        return redirect('home')

    else:
        pass

    return render(request, 'account/delete-user.html', {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def question_detail(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    question = get_object_or_404(Question, pk=id)

    return render(request, 'account/question-detail.html', {
        'question': question,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_question(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    question = get_object_or_404(Question, pk=id)

    if request.method == 'POST':
        question.status = 'published'

        question.save()

        new_notificatiion = Notification.objects.create(
            user=question.author, message=f'Hi, {question.author.first_name}, your question as been approved. Great work!! <a href="{ question.get_absolute_url() }">Check it out</a> or <a href="https://nesaacademy.com/help/#approve-question">Learn more</a>')

        new_notificatiion.save()

        send_mail('Question Approved [Nesa Academy Admin]',
                  f'Hi {question.author.first_name}, \n\nYour question "{question.title}" as been approved and made public for people to answer.\n\n {request.build_absolute_uri( question.get_absolute_url())}\n\nPlease share your question with others so people can answer.\n\nCheers', f'{settings.DEFAULT_FROM_EMAIL}', [question.author.email])

        user_profile = Profile.objects.get(user=question.author)

        user_profile.reputation += 3

        user_profile.save()

        new_notificatiion = Notification.objects.create(
            user=question.author, message=f'Hi {question.author.first_name}, you just earned additional 3 points for your reputation. Great work!! Keep it going')

        new_notificatiion.save()

        messages.success(
            request, 'You have successfully approved this question')
        return redirect('dashboard')

    return render(request, 'account/approve-question.html', {
        'question': question,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def message(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    question = get_object_or_404(Question, pk=id)

    sent = False

    if request.method == 'POST':

        message_form = MessageForm(request.POST)

        if message_form.is_valid():

            cd = message_form.cleaned_data

            user_email = question.author.email

            # send notification

            new_notificatiion = Notification.objects.create(
                user=question.author, message=f'Hi from Nesa Academy admin, please attend to the following issues below for your question titled "{question.title}". <br> {cd["message"]}<br> <a href="https://nesaacademy.com/help/#message-user">Learn more</a>')

            new_notificatiion.save()

            # send email
            send_mail('Message from Admin [Nesa Academy Admin]',
                      f"Hi {question.author.first_name}, \n\nPlease attend to the following issues below for your question titled '{question.title}'. \n\n{cd['message']}\n\nThanks.", f'{settings.DEFAULT_FROM_EMAIL}', [user_email])

            sent = True

    else:

        message_form = MessageForm()

    return render(request, 'account/message.html', {
        'sent': sent,
        'message_form': message_form,
        'question': question,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    question = get_object_or_404(Question, pk=id)

    if request.method == 'POST':

        question.delete()

        new_notificatiion = Notification.objects.create(
            user=question.author, message=f'Hi {question.author.first_name}, your question "{question.title}" as been deleted permanently. We would love for you to comply to our guidelines next time. <a href="https://nesaacademy.com/help/#delete-question">Learn more</a>')

        new_notificatiion.save()

        send_mail('Question Deleted [Nesa Academy Admin]', f'Hi "{question.author.first_name}", \n\n Your question "{question.title}" as been deleted from our database. We would love for you to comply to our guidelines next time. \n\n Thanks', f'{settings.DEFAULT_FROM_EMAIL}', [
                  question.author.email])

        user_profile = Profile.objects.get(user=question.author)

        user_profile.reputation -= 2

        user_profile.save()

        new_notificatiion = Notification.objects.create(
            user=question.author, message=f'Hi {question.author.first_name}, we just deducted two points from your reputation')

        new_notificatiion.save()

        messages.success(request, 'question deleted successfully!')
        return redirect('dashboard')

    else:

        pass

    return render(request, 'account/delete.html', {
        'question': question,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def answer_detail(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answer = get_object_or_404(Answer, pk=id)

    return render(request, 'account/answer.html', {
        'answer': answer,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_answer(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answer = get_object_or_404(Answer, pk=id)

    if request.method == 'POST':
        answer.status = 'published'

        answer.save()

        try:

            followers = FollowQuestion.objects.filter(question=answer.question)

            for follower in followers:
                new_notificatiion = Notification.objects.create(
                    user=follower.user, message=f'Hi {follower.user.first_name}, a new answer was posted for question titled "{answer.question.title}", <a href="{ answer.question.get_absolute_url() }">Check it out</a> . Note that you are receiving this notification because you follow this question.')

                new_notificatiion.save()

        except:
            pass

        new_notificatiion = Notification.objects.create(
            user=answer.author, message=f'Hi, {answer.author.first_name}, your answer as been approved. Great work!! <a href="{ answer.question.get_absolute_url() }">Check it out</a> or <a href="https://nesaacademy.com/help/#approve-question">Learn more</a>')

        new_notificatiion.save()

        send_mail('Answer Approved [Nesa Academy Admin]',
                  f'Hi {answer.author.first_name}, \n\nYour answer as been approved and made public for people to see.\n\n {request.build_absolute_uri( answer.question.get_absolute_url())} \n\nCheers', f'{settings.DEFAULT_FROM_EMAIL}', [answer.author.email])

        new_notificatiion = Notification.objects.create(
            user=answer.question.author, message=f'Hi, {answer.question.author.first_name}, {answer.author.first_name} answered your question titled "{answer.question.title}" <a href="{ answer.question.get_absolute_url() }">Check it out</a>. If you find the answer useful don\'t forget to accept the answer by clicking the red bulb')

        new_notificatiion.save()

        send_mail('Great News [Nesa Academy Admin]', f'Hi {answer.question.author.first_name}, \n\n{answer.author.first_name} answered your question titled "{answer.question.title}".\n\n {request.build_absolute_uri( answer.question.get_absolute_url())}. \n\n If you find the answer useful don\'t forget to accept the answer by clicking the red bulb. \n\nCheers', f'{settings.DEFAULT_FROM_EMAIL}', [answer.question.author.email])

        user_profile = Profile.objects.get(user=answer.author)

        user_profile.reputation += 3

        user_profile.save()

        new_notificatiion = Notification.objects.create(
            user=answer.author, message=f'Hi {answer.author.first_name}, you just earned additional 3 points for your reputation. Great work!! Keep it going')

        new_notificatiion.save()

        user_profile = Profile.objects.get(user=answer.question.author)

        user_profile.reputation += 3

        user_profile.save()

        new_notificatiion = Notification.objects.create(
            user=answer.question.author, message=f'Hi {answer.question.author.first_name}, you just earned additional 3 points for your reputation. Great work!! Keep it going')

        new_notificatiion.save()

        messages.success(request, 'You have successfully approved this answer')
        return redirect('dashboard')

    return render(request, 'account/approve-answer.html', {
        'answer': answer,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def message_for_answer(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answer = get_object_or_404(Answer, pk=id)

    sent = False

    if request.method == 'POST':

        message_form = MessageForm(request.POST)

        if message_form.is_valid():

            cd = message_form.cleaned_data

            user_email = answer.author.email

            # send notification

            new_notificatiion = Notification.objects.create(
                user=answer.author, message=f'Hi from Nesa Academy admin, please attend to the following issues below. Note that this issue emanated from your answer submitted for question titled "{answer.question.title}". <br> {cd["message"]} <hr><br> <a href="https://nesaacademy.com/help/#message-user">Learn more</a>')

            new_notificatiion.save()

            # send email
            send_mail('Message from Admin [Nesa Academy Admin]',
                      f"Hi {answer.author.first_name}, \n\nPlease attend to the following issues below.\n\nNote that this issue emanated from your answer submitted for question titled '{answer.question.title}'.\n\n{cd['message']}\n\nThanks.", f'{settings.DEFAULT_FROM_EMAIL}', [user_email])

            sent = True

    else:

        message_form = MessageForm()

    return render(request, 'account/message-for-answer.html', {
        'sent': sent,
        'message_form': message_form,
        'answer': answer,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_answer(request, id):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    answer = get_object_or_404(Answer, pk=id)

    if request.method == 'POST':

        answer.delete()

        new_notificatiion = Notification.objects.create(
            user=answer.author, message=f'Hi {answer.author.first_name}, your answer for question "{answer.question.title}" as been deleted permanently. We would love for you to comply to our guidelines next time. <a href="https://nesaacademy.com/help/#delete-question">Learn more</a>')

        new_notificatiion.save()

        send_mail('Answer Deleted [Nesa Academy Admin]',
                  f'Hi {answer.author.first_name}, \n\n Your answer for question "{answer.question.title}" as been deleted from our database. We would love for you to comply to our guidelines next time. \n\n Thanks', f'{settings.DEFAULT_FROM_EMAIL}', [answer.author.email])

        user_profile = Profile.objects.get(user=answer.author)

        user_profile.reputation -= 2

        user_profile.save()

        new_notificatiion = Notification.objects.create(
            user=answer.author, message=f'Hi {answer.author.first_name}, we just deducted two points from your reputation')

        new_notificatiion.save()

        messages.success(request, 'answer deleted successfully!')
        return redirect('dashboard')

    else:

        pass

    return render(request, 'account/delete-answer.html', {
        'answer': answer,
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def empty_notification(request):

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
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    current_date = timezone.now()
    date_less_30 = timedelta(30)

    notifications = Notification.objects.filter(
        date__lte=current_date - date_less_30)

    if request.method == 'POST':

        for notification in notifications:
            notification.delete()

        messages.success(request, 'notification deleted successfully!')
        return redirect('dashboard')

    else:

        pass

    return render(request, 'account/empty-notification.html', {

        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })
