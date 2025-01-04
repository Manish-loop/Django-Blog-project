
from django.urls import path
from .views import post_list, post_create, post_detail, post_update, post_delete

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create),
    path('<int:id>/', post_detail, name='detail'), 
    path('<int:id>/edit/', post_update, name='update'), 
    path('<int:id>/delete/', post_delete),
]