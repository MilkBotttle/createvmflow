from django.contrib import admin

from .import models

admin.site.register(models.MainProcess)
admin.site.register(models.SubP)
admin.site.register(models.MainTask)
admin.site.register(models.SubT)
