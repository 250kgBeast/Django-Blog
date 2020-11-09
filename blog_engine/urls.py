from django.urls import path

from . import views

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('tags/', views.tags_list, name='tags_list'),
    path('<str:slug>/', views.post_detail, name='post_detail'),
    path('tag/<str:slug>/', views.tag_detail, name='tag_detail')
]
