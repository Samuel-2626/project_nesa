from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('nesaacademy-admin-panel/', admin.site.urls),
    path('', include('pages.urls')),
    path('auth/', include('auth0login.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('questions/', include('questions.urls')),
    path('courses/', include('courses.urls')),
    path('quiz/', include('quiz.urls')),
    path('tutorials/', include('tutorials.urls')),
    path('articles/', include('articles.urls')),
    path('account/', include('account.urls')),
    path('notification/', include('notification.urls')),
    path('blog/', include('blog.urls')),
    path('follow/', include('Follow.urls')),
    path('newsletter/', include('newsletter.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
