from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notificationsView.as_view(), name='notifications')
]