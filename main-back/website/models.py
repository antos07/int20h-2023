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

    @property
    def is_active(self):
        return self.to is None

    def __str__(self):
        return f"{self.user} as {self.role}"


class Invitation(models.Model):
    APPROVED = 'approved'
    DECLINED = 'declined'
    PENDING = 'pending'
    STATUS_CHOICES = [(APPROVED, 'Approved'), (DECLINED, 'Declined'), (PENDING, 'Pending')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, blank=False)

    def __str__(self):
        return f"Invitation of {self.user} to {self.role}"


class JoinRequest(models.Model):
    APPROVED = 'approved'
    DECLINED = 'declined'
    PENDING = 'pending'
    STATUS_CHOICES = [(APPROVED, 'Approved'), (DECLINED, 'Declined'), (PENDING, 'Pending')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, blank=False)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Join request from {self.user} for {self.role}"
