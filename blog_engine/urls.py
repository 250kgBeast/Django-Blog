from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostsList.as_view(), name='posts_list'),
    path('tags/', views.TagsList.as_view(), name='tags_list'),
    path('tags/create', views.TagCreate.as_view(), name='tag_create'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/edit/<slug:slug>/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('tag/<slug:slug>/', views.TagPostList.as_view(), name='tag_posts_list'),
    path('tag/<slug:slug>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tag/<slug:slug>/delete/', views.TagDelete.as_view(), name='tag_delete')
]
