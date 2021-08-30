from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_blog, name='list-blog'),
    path('<slug:slug>/', views.detail_blog, name='detail-blog')
]
