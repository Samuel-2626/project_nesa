from django.shortcuts import render, get_object_or_404


from notification.models import Notification


from notification.models import Notification, Observer


from .models import Blog


# Create your views here.


def list_blog(request):
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

    blogs = Blog.objects.all()

    try:
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    return render(request, 'blog/list-blog.html', {

        'total_notifications': total_notifications,

        'blogs': blogs,
        'auth0User': auth0user,


    })


def detail_blog(request, slug):

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

    blog = get_object_or_404(Blog, slug=slug)

    try:
        get_user_profile = request.user
        auth0user = get_user_profile.social_auth.get(provider='auth0')
    except:
        auth0user = None

    return render(request, 'blog/detail-blog.html', {

        'total_notifications': total_notifications,

        'blog': blog,

        'auth0User': auth0user,

    })
