# System libraries
import socket

# Third-party Libraries

# Django modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q

# Django apps
from questions.models import Question, Answer
from notification.models import Notification
from tutorials.models import Tutorial
from articles.models import Article
from notification.models import Notification, Observer

# Current-apps modules
from .models import Institution, Course, Tutorial, Comment
from .forms import CommentForm, ReplyForm



# Create your views here.

def list_all_institution(request):

  if request.user.id != None:
      
    try:
      observer = Observer.objects.get(user=request.user)
      total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
    except:
      total_notifications = Notification.objects.filter(user=request.user).count
  else:
    total_notifications = None



  object_list = Institution.objects.all()
  institution_count = Institution.objects.all().count
  paginator = Paginator(object_list, 10)
  page = request.GET.get('page')
  try:
    institutions = paginator.page(page)
  except PageNotAnInteger:
    institutions = paginator.page(1)
  except EmptyPage:
    institutions = paginator.page(paginator.num_pages)

  return render(request, 'tutorials/institutions.html', {
    'institutions': institutions,
    'page': page,
   
    'institution_count': institution_count,
    'total_notifications': total_notifications,
  })


def detail_institution(request, institution):

  if request.user.id != None:
      
    try:
      observer = Observer.objects.get(user=request.user)
      total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
    except:
      total_notifications = Notification.objects.filter(user=request.user).count
  else:
    total_notifications = None



  institution = get_object_or_404(Institution, slug=institution)

  courses = Course.objects.filter(institution__slug=institution.slug)

  courses_count = courses.count()



  return render(request, 'tutorials/courses.html', {
    'courses': courses,
 
    'courses_count': courses_count,
    'total_notifications': total_notifications,
    'institution': institution,
  }) 


def list_tutorial(request, institution, course):

  if request.user.id != None:
      
    try:
      observer = Observer.objects.get(user=request.user)
      total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
    except:
      total_notifications = Notification.objects.filter(user=request.user).count
  else:
    total_notifications = None


  

  course = get_object_or_404(Course, slug=course)
  object_list = Tutorial.objects.filter(course__slug=course.slug)

  tutorial_count = object_list.count()

  paginator = Paginator(object_list, 15)
  page = request.GET.get('page')
  try:
    tutorials = paginator.page(page)
  except PageNotAnInteger:
    tutorials = paginator.page(1)
  except EmptyPage:
    tutorials = paginator.page(paginator.num_pages)

  return render(request, 'tutorials/list_tutorials.html', {
    'tutorials': tutorials,
    'tutorial_count': tutorial_count,
    'page': page,

    'total_notifications': total_notifications,
    'course': course,
  })


def detail_tutorial(request, tutorial_uuid):

  if request.user.id != None:
      
    try:
      observer = Observer.objects.get(user=request.user)
      total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
    except:
      total_notifications = Notification.objects.filter(user=request.user).count
  else:
    total_notifications = None




  tutorial = get_object_or_404(Tutorial, id=tutorial_uuid)

  

  # List of active comment for this question
  comments = tutorial.tutorial_comments.filter(active=True)  

  new_comment = None

  if request.method == 'POST':
    comment_form = CommentForm(data=request.POST)

    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.tutorial = tutorial
      new_comment.author = request.user
      new_comment.save()
      comment_form = CommentForm()


  else:
    comment_form = CommentForm()

  return render(request, 'tutorials/tutorial.html', {
    'tutorial': tutorial,
    'new_comment': new_comment,
    'comment_form': comment_form,
    'comments': comments,
   
    'total_notifications': total_notifications,
  })


@login_required
def edit_comment(request, id, uuid):
    


    if request.user.id != None:
      
      try:
        observer = Observer.objects.get(user=request.user)
        total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
      except:
        total_notifications = Notification.objects.filter(user=request.user).count
    else:
      total_notifications = None

    comment = Comment.objects.get(id=id)
    tutorial = Tutorial.objects.get(id=uuid)

    if comment.author != request.user:
      messages.success(request, '<strong>Access Denied:</strong> You are not the author of this comment ', extra_tags='safe')
      return redirect(f'https://www.nesaacademy.com/tutorials/{uuid}')


    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.save()
            comment_form.save_m2m()

           

            messages.success(request, 'comment edited successfully!')
            return redirect(f'https://www.nesaacademy.com/tutorials/{uuid}')
  
    else:
        comment_form = CommentForm(instance=comment)
        
    return render(request, 'tutorials/edit.html', {
        'comment_form': comment_form,
      
        'total_notifications': total_notifications,
        'comment': comment,
        'tutorial': tutorial,
    })
    

@login_required
def delete_comment(request, id, uuid):

    if request.user.id != None:
      
      try:
        observer = Observer.objects.get(user=request.user)
        total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
      except:
        total_notifications = Notification.objects.filter(user=request.user).count
    else:
      total_notifications = None
    


    comment = Comment.objects.get(id=id)
    tutorial = Tutorial.objects.get(id=uuid)



    if comment.author != request.user:
      messages.success(request, '<strong>Access Denied:</strong> You are not the author of this comment', extra_tags='safe')
      return redirect(f'https://www.nesaacademy.com/tutorials/{uuid}')

 
    
    if request.method == 'POST':
        comment.delete()
       
        messages.success(request, 'comment deleted successfully!')
        return redirect(f'https://www.nesaacademy.com/tutorials/{uuid}')
  
    else:
        comment_form = CommentForm()

    return render(request, 'tutorials/delete.html', {
        'comment_form': comment_form,
        'comment': comment,
  
        'total_notifications': total_notifications,
        'tutorial': tutorial,


  })


def tutorial_search(request):



  if request.user.id != None:
      
    try:
      observer = Observer.objects.get(user=request.user)
      total_notifications = Notification.objects.filter(user=request.user, date__gt=observer.date).count
      
    except:
      total_notifications = Notification.objects.filter(user=request.user).count
  else:
    total_notifications = None

 
  query_tut = None
  results = []
  if 'query_tutorial' in request.GET:
  
    query_tut = request.GET.get('query_tutorial')

    # search_vector = SearchVector('question', 'answer')
    # search_query = SearchQuery(query_tut)
    # results = Tutorial.objects.all().annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
  
    results = Tutorial.objects.filter(
            Q(question__icontains=query_tut) | Q(answer__icontains=query_tut)
        )

  return render(request, 'tutorials/search.html', {

    'query_tut': query_tut,
    'results': results,

 
    'total_notifications': total_notifications,
  })
