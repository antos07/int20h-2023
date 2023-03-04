from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from website.forms import RegistrationForm
from website.models import Project, Participation, Invitation, JoinRequest


class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'test_app/register.html'

    def get_success_url(self):
        return reverse('website:login')


class ProfileView(generic.DetailView):
    model = User
    context_object_name = 'showed_user'
    template_name = 'test_app/profile.html'


class UserProjectsView(generic.ListView):
    template_name = 'test_app/user_projects.html'
    context_object_name = 'projects'
    requested_user: User

    def dispatch(self, request, *args, **kwargs):
        self.requested_user = get_object_or_404(User, pk=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Participation.objects.filter(user=self.requested_user).order_by('-since')

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['requested_user'] = self.requested_user
        context_data['pending_invitations'] = []
        context_data['pending_join_requests'] = []
        if self.requested_user == self.request.user:
            context_data['pending_invitations'] = (Invitation.objects
                                                   .filter(user=self.requested_user, status=Invitation.PENDING)
                                                   .order_by('-timestamp'))
            context_data['pending_join_requests'] = (JoinRequest.objects
                                                     .filter(user=self.requested_user, status=JoinRequest.PENDING)
                                                     .order_by('-timestamp'))
        return context_data
