from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Project)
admin.site.register(models.Role)
admin.site.register(models.Skill)
admin.site.register(models.Participation)
admin.site.register(models.Invitation)
admin.site.register(models.JoinRequest)
