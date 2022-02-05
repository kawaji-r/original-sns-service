from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('edit/', views.ProfileEdit.as_view(), name='edit'),
    path('<uuid:pk>/post/', views.ProfileDetail.as_view(), name='detail_post'),
    path('<uuid:pk>/post_reply/', views.ProfileDetail.as_view(), name='detail_post_reply'),
    path('<uuid:pk>/media/', views.ProfileDetail.as_view(), name='detail_media'),
    path('<uuid:pk>/like/', views.ProfileDetail.as_view(), name='detail_like'),
    path('follow/', views.FollowControl.as_view(), name='follow'),
    path('unfollow/', views.FollowControl.as_view(), name='unfollow'),
    path('follow-list/<uuid:pk>/', views.FollowList.as_view(), name='followlist'),
    path('follower-list/<uuid:pk>/', views.FollowList.as_view(), name='followerlist'),
    path('deactivate/<uuid:pk>/', views.Deactivate.as_view(), name='deactivate'),
]
