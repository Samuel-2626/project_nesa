# System Libraries
import socket

# Third-party Libraries
from taggit.models import Tag
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

# Django modules
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Django apps
from notification.models import Notification
from articles.models import Article
from account.models import Profile
from notification.models import Notification, Observer

# Current-app modules
from .models import Article, Comment, PostViews, PostLikesOrDislikes
from .forms import EmailPostForm, CommentForm, PostForm
from .serializers import PostLikesOrDislikesSerializer


def post_list(request, tag_slug=None):

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

    object_list = Article.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 50)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'article/post/list.html', {
                  'page': page,
                  'posts': posts,
                  'tag': tag,

                  'total_notifications': total_notifications,
                  })


def post_detail(request, year, month, day, post):

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

    hostname = socket.gethostname()

    ip_address = socket.gethostbyname(hostname)

    post = get_object_or_404(Article, slug=post,
                             status='published',
                             created__year=year,
                             created__month=month,
                             created__day=day)

    try:
        new_view = PostViews(article=post, host=hostname, ip=ip_address)
        new_view.save()
        post.views += 1
        post.save()
    except:
        pass

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.article = post
            # Save the comment to the database
            new_comment.author = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Article.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)

    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-created')[:4]

    return render(request, 'article/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,

        'total_notifications': total_notifications,
    })


def post_share(request, post_id):

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
    post = get_object_or_404(Article, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message,
                      f'{settings.DEFAULT_FROM_EMAIL}', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'article/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent,

        'total_notifications': total_notifications,
    })


@login_required
def post_article(request):

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
    new_post = None

    if request.user.profile.reputation < 100:

        messages.success(request, '<b>Access Denied:</b> You need atleast 100 reputation to post an article <a href="/help/#posting-article" style="color:#DDAF94;">Learn more</a>', extra_tags='safe')

        return redirect('articles:post_list')

    if request.method == 'POST':

        post_form = PostForm(data=request.POST, files=request.FILES)

        if post_form.is_valid():

            new_post = post_form.save(commit=False)

            new_post.author = request.user

            new_post.save()

            post_form.save_m2m()

            # get the profile of the current user
            user_profile = Profile.objects.get(user=request.user)

            # give the user 5 reputation for asking a question
            user_profile.reputation += 5

            # save this new reputation
            user_profile.save()

            new_notificatiion = Notification.objects.create(
                user=request.user, message=f'Hi {request.user.first_name}, you have received an addition of five points for your reputation for posting a new article')

            # save notification in database
            new_notificatiion.save()

            messages.success(request, 'posted successfully')

            return redirect('articles:post_list')

        else:
            post_form = PostForm(data=request.POST, files=request.FILES)

    else:

        post_form = PostForm()

    return render(request, 'article/post/new.html', {
        'new_post': new_post,
        'post_form': post_form,

        'total_notifications': total_notifications,
    })


@login_required
def edit_comment(request, id, slug):

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

    comment = Comment.objects.get(id=id)
    post = Article.objects.get(slug=slug)

    if comment.author != request.user:
        messages.success(
            request, '<strong>Access Denied:</strong> You are not the author of this comment ', extra_tags='safe')
        return redirect(f'https://nesaacademy.com{post.get_absolute_url()}')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.save()
            comment_form.save_m2m()

            messages.success(request, 'comment edited successfully!')
            return redirect(f'https://nesaacademy.com{post.get_absolute_url()}')

    else:
        comment_form = CommentForm(instance=comment)

    return render(request, 'article/post/edit-comment.html', {
        'comment_form': comment_form,

        'total_notifications': total_notifications,
        'comment': comment,
        'post': post,
    })


@login_required
def delete_comment(request, id, slug):

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

    comment = Comment.objects.get(id=id)
    post = Article.objects.get(slug=slug)

    if comment.author != request.user:
        messages.success(
            request, '<strong>Access Denied:</strong> You are not the author of this comment', extra_tags='safe')
        return redirect(f'https://nesaacademy.com{post.get_absolute_url()}')

    if request.method == 'POST':
        comment.delete()

        messages.success(request, 'comment deleted successfully!')
        return redirect(f'https://nesaacademy.com/{post.get_absolute_url()}')

    else:
        comment_form = CommentForm()

    return render(request, 'article/post/delete-comment.html', {
        'comment_form': comment_form,
        'comment': comment,

        'total_notifications': total_notifications,
        'post': post,

    })


def article_search(request):

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

    query_articles = None
    results = []
    if 'query_art' in request.GET:

        query_articles = request.GET.get('query_art')

        # search_vector = SearchVector('title', 'body')
        # search_query = SearchQuery(query_articles)
        # results = Article.objects.all().annotate(search=search_vector, rank=SearchRank(
        #     search_vector, search_query)).filter(search=search_query).order_by('-rank')

        results = Article.published.filter(
            Q(title__icontains=query_articles) | Q(body__icontains=query_articles)
        )

    return render(request, 'article/post/search.html', {

        'query_articles': query_articles,
        'results': results,


        'total_notifications': total_notifications,
    })


class GetPostUserStatus(generics.ListAPIView):

    serializer_class = PostLikesOrDislikesSerializer

    def get_queryset(self):

        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']

        return PostLikesOrDislikes.objects.filter(author__pk=user_id, article_id=post_id)


class LikePost(APIView):

    def post(self, request, user_id, post_id):

        user = User.objects.get(pk=user_id)
        article = Article.objects.get(id=post_id)

        new_like = PostLikesOrDislikes(
            author=user, article=article, status='like')

        new_like.save()

        return Response({"message": "Liked Successfully"})


class DisLikePost(APIView):

    def post(self, request, user_id, post_id):

        user = User.objects.get(pk=user_id)
        article = Article.objects.get(id=post_id)

        new_like = PostLikesOrDislikes(
            author=user, article=article, status='dislike')

        new_like.save()

        return Response({"message": "Disliked Successfully"})


class IncreaseArticle(APIView):

    def post(self, request, post_id):

        article = get_object_or_404(Article, id=post_id)

        article.likes += 1

        article.save()

        return Response({"message": "Successfully Increased"})


class IncreaseDislikeArticle(APIView):

    def post(self, request, post_id):

        article = get_object_or_404(Article, id=post_id)

        article.dislikes += 1

        article.save()

        return Response({"message": "Successfully Increased"})


class DecreaseArticle(APIView):

    def post(self, request, post_id):

        article = get_object_or_404(Article, id=post_id)

        article.likes -= 1

        article.save()

        return Response({"message": "Successfully Decreased"})


class DecreaseDislikeArticle(APIView):

    def post(self, request, post_id):

        article = get_object_or_404(Article, id=post_id)

        article.dislikes -= 1

        article.save()

        return Response({"message": "Successfully Decreased"})


class RemoveDislikeToLike(APIView):

    def post(self, request, user_id, post_id):

        article = PostLikesOrDislikes.objects.get(
            author__pk=user_id, article_id=post_id)

        article.status = 'like'

        article.save()

        return Response({"message": "Successfully Changed"})


class RemoveLikeToDisLike(APIView):

    def post(self, request, user_id, post_id):

        article = PostLikesOrDislikes.objects.get(
            author__pk=user_id, article_id=post_id)

        article.status = 'dislike'

        article.save()

        return Response({"message": "Successfully Changed"})
