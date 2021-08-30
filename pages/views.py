# System Libraries

# Third-party Libraries

# Django modules
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.conf import settings

# Django apps

from notification.models import Notification


from notification.models import Notification, Observer

# Current-app modules
from .forms import ContactForm


def home(request):

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

    get_user_profile = request.user

    try:
        auth0user = get_user_profile.social_auth.get(provider='auth0')

    except:
        auth0user = None

    if request.method == 'GET':
        form = ContactForm()

    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            message = f'This message was from \n\n{from_email} \n\n {message}'
            try:
                send_mail(subject, message, from_email,
                          [settings.DEFAULT_FROM_EMAIL])
                print(from_email)
                print(settings.DEFAULT_FROM_EMAIL)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    return render(request, "home.html", {
        'form': form,

        'total_notifications': total_notifications,
        'auth0User': auth0user,
    })


def successView(request):

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

    return render(request, "pages/email-success.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


def CodeOfConduct(request):

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

    return render(request, "pages/code-of-conduct.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


@login_required
def Users(request):

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

    total_users = User.objects.filter(is_active=True).count

    user_list = User.objects.filter(is_active=True)

    user_query = request.GET.get('q_user')

    if user_query:

        search_vector = SearchVector('first_name', 'last_name')

        search_query = SearchQuery(user_query)
        user_list = User.objects.filter(is_active=True).annotate(search=search_vector, rank=SearchRank(
            search_vector, search_query)).filter(search=search_query).order_by('-rank')

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 200)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'pages/users.html', {
        'users': users,
        'total_users': total_users,

        'auth0User': auth0user,

        'user_query': user_query,
        'page': page,
        'total_notifications': total_notifications,

    })


def Help(request):

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

    return render(request, "pages/help.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


def Privacy(request):

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

    return render(request, "pages/privacy.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


def Faq(request):

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

    return render(request, "pages/faq.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,

    })


def Terms(request):

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

    return render(request, "pages/terms.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })


def Gpa(request):

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

    return render(request, "pages/gpa.html", {
        'auth0User': auth0user,
        'total_notifications': total_notifications,
    })
