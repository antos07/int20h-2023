from django.urls import reverse
from django.views import generic

from website.forms import RegistrationForm


class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'test_app/register.html'
    success_url = reverse('website:login')
