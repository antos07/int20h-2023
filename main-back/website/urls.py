from django.contrib.auth.views import LoginView
from django.urls import path

from website.views import RegisterView

app_name = 'website'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='test_app/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
