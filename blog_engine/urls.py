from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts_list'),
    path('tags/', views.TagsListView.as_view(), name='tags_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/edit/<str:slug>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<str:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tag/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail')
]
