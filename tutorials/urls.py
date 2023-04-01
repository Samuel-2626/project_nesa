from django.urls import path
from .views import list_all_institution, detail_institution, list_tutorial, detail_tutorial, edit_comment, delete_comment, tutorial_search

urlpatterns = [
    path('search/', tutorial_search, name='tutorial_search'),
    path('institutions/', list_all_institution, name="list_all_institution"),
    path('institutions/<slug:institution>/', detail_institution, name="detail_institution"),
    path('institutions/<slug:institution>/<slug:course>/', list_tutorial, name="list_tutorial"),
    path('<str:tutorial_uuid>/', detail_tutorial, name="detail_tutorial"),
    path('comment/<int:id>/<str:uuid>/edit', edit_comment, name="edit_comment"),
    path('comment/<int:id>/<str:uuid>/delete', delete_comment, name="delete_comment"),
    

    
]
