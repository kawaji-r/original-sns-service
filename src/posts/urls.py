from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostIndexView.as_view(), name='index'),
    path('<uuid:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('delete/<uuid:pk>/', views.PostDeleteView.as_view(), name='delete'),
    path('like/', views.LikeView.as_view(), name='like'),
    path('unlike/', views.LikeView.as_view(), name='unlike'),
    path('repost/', views.RepostView.as_view(), name='repost'),
    path('unrepost/', views.RepostView.as_view(), name='unrepost'),
    path('bookmark/', views.PostBookmarkView.as_view(), name='bookmark'),
    path('bookmarking/', views.BookmarkView.as_view(), name='bookmarking'),
    path('unbookmarking/', views.BookmarkView.as_view(), name='unbookmarking'),
    path('reply/', views.ajax_reply, name='ajax_reply')
]