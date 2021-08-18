"""Definiuje wzorce adresów URL dla blogs"""

from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    #Strona główna
    path('',views.index, name='index'),
    # Strona z postami
    path('posts/', views.posts, name='posts'),
    # Dodawanie nowego postu
    path('new_post/', views.new_post, name='new_post'),
    # Edycja postu
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]