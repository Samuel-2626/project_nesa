from django.urls import path

from .views import home, successView, CodeOfConduct, Users, Help, Faq, Terms, Privacy, Gpa


urlpatterns = [


    path('', home, name="home"),
    path('success/', successView, name='success'),
    path('code-of-conduct/', CodeOfConduct, name='code-of-conduct'),
    path('users/', Users, name='users'),
    path('help/', Help, name='help'),
    path('faq/', Faq, name='faq'),
    path('terms/', Terms, name='terms'),
    path('privacy/', Privacy, name='privacy'),
    path('gpa-calculator/', Gpa, name='gpa'),


]
