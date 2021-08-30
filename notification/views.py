# Django modules

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Django apps

from notification.models import Notification


# Current-app modules
from .models import Notification, Observer

from datetime import timedelta


@login_required
def show_notification(request):

    try:
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    object_list = Notification.objects.filter(user=request.user)

    try:
        observer = Observer.objects.get(user=request.user)
        observer.date = timezone.now()
        observer.save()
    except:
        observer = Observer.objects.create(user=request.user)
        observer.save()

    total_notifications = Notification.objects.filter(
        user=request.user, date__gt=observer.date).count

    observer.date = observer.date - timedelta(days=1)

    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    return render(request, 'notification/my-notification.html', {

        'auth0User': auth0user,
        'total_notifications': total_notifications,
        'notifications': notifications,
        'observer': observer,
        'page': page,

    })
