from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

from website.forms import RegistrationForm


class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'test_app/register.html'

    def get_success_url(self):
        return reverse('website:login')


class ProfileView(generic.DetailView):
    model = User
    context_object_name = 'showed_user'
    template_name = 'test_app/profile.html'
