from django.urls import path
from posts.views import feed, ini, create_post, post_detail, view_profile, edit_profile, delete_comment, delete_post, follow, unfollow, like_post

urlpatterns = [
    path('', ini, name='ini'),
    path('feed/', feed, name='feed'),
    path('feed/create', create_post, name='create_posts'),
    path('feed/<int:id>', post_detail, name="post_detail"),
    path('feed/user/<str:username>', view_profile, name="view_profile"),
    path('feed/user/<str:username>/edit_profile', edit_profile, name="edit_profile"),
    path('feed/<int:post_id>/comment/<int:comment_id>/delete', delete_comment, name="delete_comment"),
    path('feed/<int:post_id>/delete', delete_post, name="delete_post"),
    path('feed/user/<str:username>/follow', follow, name="follow"),
    path('feed/user/<str:username>/unfollow', unfollow, name="unfollow"),
    path('feed/<int:post_id>/like', like_post, name="like")
] 
