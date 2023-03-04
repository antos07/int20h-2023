from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=32, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_mentor = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    since = models.DateField()
    to = models.DateField(null=True)
