from typing import Iterable

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from website.forms import RegistrationForm
from website.models import Project, Participation, Invitation, JoinRequest, Skill, Role


class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'website/register.html'

    def get_success_url(self):
        return reverse('website:login')


class ProfileView(generic.DetailView):
    model = User
    context_object_name = 'showed_user'
    template_name = 'website/profile.html'


class UserProjectsView(generic.ListView):
    template_name = 'website/user_projects.html'
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


class ProjectListView(generic.ListView):
    model = Project
    template_name = 'website/projects.html'
    context_object_name = 'projects'

    skills: Iterable[Skill]
    selected_skills: set[Skill]

    def dispatch(self, request, *args, **kwargs):
        self.skills = Skill.objects.order_by('name').all()
        self.selected_skills = self.get_selected_skills()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.selected_skills:
            return Project.objects.order_by('name')
        roles_with_selected_skills = Role.objects.filter(skills__in=self.selected_skills).values_list('id')
        not_selected_skills = set(self.skills) - set(self.selected_skills)
        roles_without_selected_skills = Role.objects.filter(skills__in=not_selected_skills).values_list('id')
        roles_with_only_selected_skills = roles_with_selected_skills.difference(roles_without_selected_skills)
        return Project.objects.filter(role__id__in=roles_with_only_selected_skills).distinct().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['skills'] = self.skills
        context_data['selected_skills'] = self.selected_skills
        return context_data

    def get_selected_skills(self) -> set[Skill]:
        selected = set()
        for skill in self.skills:
            if f'skill_{skill.pk}' in self.request.GET:
                selected.add(skill)
        return selected


class UserListView(generic.ListView):
    model = User
    template_name = 'website/users.html'
    context_object_name = 'users'


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'website/project_detail.html'


@login_required(login_url='/login')
def create_join_request(request, role_id: int):
    user = request.user
    role = get_object_or_404(Role, pk=role_id)

    if not JoinRequest.objects.filter(user=user, role=role):
        JoinRequest.objects.create(user=user, role=role)

    return redirect(reverse('website:user_projects', args=(user.id,)))


@login_required(login_url='/login')
def generate_cv(request):
    user = request.user

    cv_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'image_url': 'https://www.zdnet.com/a/img/resize/22996632853fd12eeffc973ecdafa55e4439ef6c/2022/09/05/c70fdeec-fd32-4d1c-96fe-d5dfe2f63da4/img-1001.jpg?auto=webp&fit=crop&height=1200&width=1200',
        'email': user.email,
        'linkedIn': user.profile.linkedin,
        'phoneNumber': user.profile.phone,
        'telegram': user.profile.telegram,
        'skills': [skill.name for skill in user.profile.skills.all()],
        'projects': [
            {
                'name': project.role.project.name,
                'role': project.role.name,
                'since': str(project.since),
                'till': str(project.to) if project.to else None,
                'roleDescription': project.role.description,
                'projectUrl': reverse('website:project_detail', args=(project.role.project.pk,))
            }
            for project in user.participation_set.all()
        ]
    }

    response = requests.post('http://apiint20h-env.eba-43pkh2q3.ap-northeast-1.elasticbeanstalk.com/pdf/generate',
                             json=cv_data)
    response.raise_for_status()
    return HttpResponse(response.content, content_type='application/pdf')
