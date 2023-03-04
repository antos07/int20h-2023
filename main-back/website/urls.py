from django.contrib.auth.views import LoginView
from django.urls import path

from website.views import RegisterView, ProfileView, UserProjectsView, ProjectListView, UserListView

app_name = 'website'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='website/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/projects', UserProjectsView.as_view(), name='user_projects'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('users/', UserListView.as_view(), name='users'),
]
