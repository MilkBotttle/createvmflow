from django.db import models
from django.conf import settings

from viewflow.models import Process, Task

class CreatevmProcess(Process):
    username = models.CharField(max_length=150)
    cpu_cores = models.PositiveIntegerField(default=0)
    disk_size = models.PositiveIntegerField(default=0)
    memory_size = models.PositiveIntegerField(default=0)
    os_type = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'CreateVM process list'
        permissions = [
            ('can_start_request','Can start createvm request'),
            ('can_assign_approver','Can assign approver'),
            ('can_approve_request','Can approve request')
        ]

class CreatvmTask(Task):
    class Meta:
        proxy = True

class ProcessApproverAndAns(models.Model):
    process = models.ForeignKey(CreatevmProcess, blank=True, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(CreatvmTask, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    approve = models.BooleanField(default=True)

    
