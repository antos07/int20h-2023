from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from website.views import RegisterView, ProfileView, UserProjectsView, ProjectListView, UserListView, ProjectView, \
    create_join_request, generate_cv

app_name = 'website'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='website/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>', ProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/projects', UserProjectsView.as_view(), name='user_projects'),
    path('projects/join/role/<int:role_id>', create_join_request, name='join_request'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>', ProjectView.as_view(), name='project_detail'),
    path('cv', generate_cv, name='cv'),
    path('', RedirectView.as_view(pattern_name='website:projects'), name='home'),
]
