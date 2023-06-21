from django.urls import path
from . import views

urlpatterns = [
    path('post_user/', views.post_user),
    path('get_users/', views.get_users),
    path('add_user/', views.add_user),
    path('', views.HomeView.as_view(), name='home.html'),
]