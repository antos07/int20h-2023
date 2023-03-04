from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=32, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_mentor = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.project}: {self.name}'


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    since = models.DateField()
    to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} as {self.role}"


class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations_set')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sent_invitations_set')
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

    def __str__(self):
        return f"From {self.user} to {self.role}"
