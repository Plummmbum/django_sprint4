from django.urls import include, path

from blog import views

app_name = 'blog'

posts_urls = [
    path(
        'create/',
        views.create_post,
        name='create_post'
    ),
    path(
        '<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        '<int:post_id>/edit/',
        views.edit_post,
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    path(
        '<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
]

urlpatterns = [
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'edit_profile/',
        views.edit_profile,
        name='edit_profile'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path('', views.index, name='index'),
    path('posts/', include(posts_urls)),
]
