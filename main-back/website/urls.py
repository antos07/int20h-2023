from django.contrib.auth.views import LoginView
from django.urls import path

app_name = 'website'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='test_app/login.html'), name='login'),
]
