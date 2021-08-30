from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_notification, name='my-notification'),
]
